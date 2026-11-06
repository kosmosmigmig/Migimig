from pathlib import Path
r=Path(__file__).resolve().parents[1] / 'src/video_core';s=(r/'memory_manager.cpp').read_text()
def fn(needle):
 start=s.index(needle);a=s.index('{',start);depth=1;i=a+1
 while depth:
  if s[i]=='{':depth+=1
  elif s[i]=='}':depth-=1
  i+=1
 return s[start:i]
small=fn('GPUVAddr MemoryManager::PageTableOp');big=fn('GPUVAddr MemoryManager::BigPageTableOp')
def call(body):
 start=body.index('RecordMapChange(');return body[start:body.index(';',start)+1]
code='''#include <algorithm>
#include <array>
#include <atomic>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <random>
using u64=uint64_t; using GPUVAddr=u64;
namespace Common { template<class T> T AlignUp(T n,T align){return (n+align-1)&~(align-1);} }
struct MemoryManager {
std::atomic<u64> map_serial{};size_t unique_identifier;mutable size_t walks{};
struct MapChange {u64 serial;GPUVAddr gpu_addr;u64 size;};
static constexpr size_t map_change_ring=256;
std::array<MapChange,256> map_changes{};mutable std::mutex changes_guard;
static constexpr u64 page_size=4096,page_mask=4095,big_page_size=65536,big_page_mask=65535;
std::array<u64,1024> pages{};
MemoryManager(size_t id):unique_identifier(id){for(u64 i=0;i<pages.size();++i)pages[i]=i*page_size;}
void RecordMapChange(GPUVAddr,u64);bool RangeUnchangedSince(u64,u64,GPUVAddr,u64) const;
size_t MaxContinuousRange(GPUVAddr,size_t) const;
size_t MaxContinuousRangeUncached(GPUVAddr addr,size_t size) const {
 ++walks; size_t n=0;u64 next=0;
 while(n<size){auto at=addr+n;auto p=at/page_size;if(p>=pages.size()||pages[p]==~u64{0})break;
 u64 phys=pages[p]+(at&page_mask);if(n&&phys!=next)break;
 size_t take=std::min<size_t>(size-n,page_size-(at&page_mask));n+=take;next=phys+take;}
 return n;
}
void Change(GPUVAddr gpu_addr,u64 size,u64 device,bool big){
 u64 step=big?big_page_size:page_size;
 for(u64 off=0;off<size;off+=step){u64 start=(gpu_addr+off)&~(step-1);
 for(u64 pos=start;pos<start+step;pos+=page_size)pages[pos/page_size]=device==~u64{0}?device:device+(pos-start)+off;}
 std::unique_lock<std::mutex> lock(changes_guard);
 if(big){BIGCALL}else{SMALLCALL}
}
};
'''.replace('BIGCALL',call(big)).replace('SMALLCALL',call(small))
for name in ['size_t MemoryManager::MaxContinuousRange(', 'void MemoryManager::RecordMapChange(', 'bool MemoryManager::RangeUnchangedSince(']:code+=fn(name)+'\n'
code+='''int main(){
 MemoryManager m(1);
 // A 4 KiB Unmap updates the big-page entry too (Unmap invokes both table operations).
 auto before=m.MaxContinuousRange(32768,8192);if(before!=8192)return 10;
 m.Change(0,4096,~u64{0},true);
 auto actual=m.MaxContinuousRange(32768,8192),expected=m.MaxContinuousRangeUncached(32768,8192);
 if(actual!=expected){std::cerr<<"FAIL big-page partial unmap: cached="<<actual<<" expected="<<expected<<"\\n";return 1;}
 MemoryManager n(2);std::mt19937 rng(163256);u64 checksum=0;
 for(int i=0;i<100000;++i){
 if(i%4==0){u64 size=1+rng()%8192;bool big=rng()%8==0;u64 addr=(rng()%960)*4096ULL;
 n.Change(addr,size,(rng()%3==0)?~u64{0}:u64(rng()%1024)*4096,big);}
 u64 addr=(rng()%1000)*4096ULL+rng()%4096;u64 size=1+rng()%65536;
 auto a=n.MaxContinuousRange(addr,size),b=n.MaxContinuousRangeUncached(addr,size);if(a!=b){std::cerr<<"FAIL random "<<i<<"\\n";return 2;}checksum+=a;
 // Repeat a smaller request, exercising the capped-result cache.
 if(n.MaxContinuousRange(addr,size/2)!=n.MaxContinuousRangeUncached(addr,size/2))return 3;
 }
 MemoryManager z(3);auto base=z.MaxContinuousRange(0,8192);auto serial=z.map_serial.load();
 for(int i=0;i<256;++i)z.Change(0x20000,4096,0x20000,false);
 if(!z.RangeUnchangedSince(serial,z.map_serial,0,8192))return 4;
 z.Change(0x20000,4096,0x20000,false);
 if(z.RangeUnchangedSince(serial,z.map_serial,0,8192))return 5;
 if(z.MaxContinuousRange(0,8192)!=base)return 6;
 // Exact boundaries, overlapping remaps, and zero-length queries.
 serial=z.map_serial.load();z.Change(8192,4096,~u64{0},false);
 if(!z.RangeUnchangedSince(serial,z.map_serial,0,8192))return 7;
 z.Change(4096,4096,~u64{0},false);
 if(z.MaxContinuousRange(0,8192)!=4096||z.MaxContinuousRange(0,0)!=0)return 8;
 MemoryManager p(4);p.MaxContinuousRange(0,8192);auto start=p.walks;
 for(int i=0;i<10000;++i){p.Change(0x20000,4096,0x20000,false);if(p.MaxContinuousRange(0,8192)!=8192)return 9;}
 std::cout<<"PASS 100000 random comparisons + smaller requests + partial big-page unmap + history/boundary cases. checksum="<<checksum<<" unrelated_change_walks="<<p.walks-start<<"\\n";
}
'''
import sys
Path(sys.argv[1]).write_text(code)

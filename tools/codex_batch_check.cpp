#include <array>
#include <cstdio>
#include <random>
#include <map>
#include "dynarmic/tests/A64/testenv.h"
int main() {
    A64TestEnv env;
    Dynarmic::A64::UserConfig conf{};
    conf.callbacks = &env;
    Dynarmic::A64::Jit jit{conf};
    std::mt19937_64 rng{711239};
    unsigned long long hash = 1469598103934665603ULL;
    auto mix = [&](u64 v) {hash ^= v; hash *= 1099511628211ULL;};
    for (int trial=0; trial<1000; ++trial) {
        jit.ClearCache();
        env.modified_memory.clear(); env.code_mem.clear();
        for (int k=0;k<80;++k) {
            const u32 d=rng()%28, n=rng()%28, m=rng()%28;
            switch(rng()%8) {
            case 0: env.code_mem.push_back(0x8b000000|(m<<16)|(n<<5)|d); break;
            case 1: env.code_mem.push_back(0xab000000|(m<<16)|(n<<5)|d); break;
            case 2: env.code_mem.push_back(0xb4000040|n); break; // cbz +8
            case 3: env.code_mem.push_back(0xb5000040|n); break;
            case 4: env.code_mem.push_back(0x36000040|((rng()%32)<<19)|n); break;
            case 5: env.code_mem.push_back(0x54000040|(rng()%14)); break;
            case 6: env.code_mem.push_back(0xf9000000|((rng()%16)<<10)|(28<<5)|d); break;
            case 7: env.code_mem.push_back(0xf9400000|((rng()%16)<<10)|(28<<5)|d); break;
            }
        }
        env.code_mem.push_back(0xd503201f); // nop, landing for the last conditional
        env.code_mem.push_back(0x14000000);
        for(int i=0;i<31;++i) jit.SetRegister(i, rng()%3==0?0:rng());
        jit.SetRegister(28,0x10000); jit.SetPC(0); jit.SetPstate(0);
        env.ticks_left=1000; jit.Run();
        for(auto v:jit.GetRegisters())mix(v);
        mix(jit.GetPC()); mix(jit.GetPstate());
        std::map<u64,u8> ordered;
        for(auto [a,b]:env.modified_memory) ordered[a]=b;
        for(auto [a,b]:ordered){mix(a);mix(b);}
    }
    std::printf("1000 programs: %016llx\n",hash);
}

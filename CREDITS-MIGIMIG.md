# Credits and provenance

Migimig is primarily integration work. The original emulator architecture and the majority of its code belong to the upstream projects and contributors, not to Migimig.

- [Lichii / zortos293](https://github.com/zortos293/Lichii): immediate upstream, rendering, synchronization and performance work.
- [Frizti / Lichii](https://github.com/Frizti/Lichii): Frizti v2 integration base and its fixes, including the built-in Dynamic FPS patch credited upstream to Dark.
- [Eglantine / Djihads80](https://github.com/Djihads80/Eglantine), Eden, yuzu and Sudachi: inherited emulator work; retain their original notices and Git authorship.
- [Selevet](https://github.com/sylvieistaken/selevet-eglantine): inspiration for the Mario Kart World preflush adaptation. This is a scoped adaptation, not a claim that Selevet was wholly merged.
- Nolar-Hack: retained authored JIT optimizations and texture traversal work (see Git history).
- Matt Artist and all other contributors: inherited buffer binding, uniform upload and other work remains attributed in Git history.
- [RsMan-Dev](https://github.com/RsMan-Dev/Lichii): pending occlusion report synchronization, adapted from commit 42cbd65122b729ec633307c36ff22e00d94e65fa.

## Selected upstream integrations

- [Lichii PR #178](https://github.com/zortos293/Lichii/pull/178) — tibzejoker: video_core: skip the instance loop writes the split back ignores. Only the relevant portions were integrated; this does not claim the complete PR is present.
- [Lichii PR #232](https://github.com/zortos293/Lichii/pull/232) — PantACRO4life: common: keep time-critical threads on the performance cores of hybrid CPUs on Windows. Only the relevant portions were integrated; this does not claim the complete PR is present.
- [Lichii PR #235](https://github.com/zortos293/Lichii/pull/235) — Feralnet: video_core: queue a safe read's flush on the split's back thread (EDEN_NX2_SPLIT_SAFE_READS). Only the relevant portions were integrated; this does not claim the complete PR is present.
- [Lichii PR #250](https://github.com/zortos293/Lichii/pull/250) — tibzejoker: video_core: skip GPU-write invalidations of caches with nothing on those pages. Only the relevant portions were integrated; this does not claim the complete PR is present.
- [Lichii PR #264](https://github.com/zortos293/Lichii/pull/264) — Kajcsi: buffer_cache: arm read traps only on the pages not armed yet. Only the relevant portions were integrated; this does not claim the complete PR is present.
- [Lichii PR #267](https://github.com/zortos293/Lichii/pull/267) — RsMan-Dev: How I got 60 FPS on my config: Ryzen 9 9950X3D + RTX 4080 (Ocarina of Time). Only the relevant portions were integrated; this does not claim the complete PR is present.

## Local work

The unnamed project lead provided project direction, research priorities, coordination of AI-assisted work, integration choices, visual assessment, testing and validation. Codex and Claude assisted with research and code changes. The selective continuous-range invalidation work was prepared with Claude and integrated and supplemented with regression checks by Codex. The local Mario Kart-specific preflush adaptation, integration adjustments and diagnostic changes are documented in Git history.

This list highlights provenance; it does not replace or exhaust the original contributor history and copyright notices. No upstream author's endorsement is implied.

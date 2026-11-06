# Migimig 0.1 — initial experimental reference

- Frizti v2 base with Nolar-authored JIT changes and selected texture traversal improvements.
- Selective continuous-range cache invalidation with regression coverage.
- Selected Lichii cache page filtering, hybrid CPU core placement, split safe reads and selective read-trap arming.
- Mario Kart World-only Selevet-inspired preflush behaviour; the equivalent Zelda experiment was rejected and is not enabled.
- Retains the inherited decoder/fence handling used to address the second-race Mario Kart issue.
- Adapted pending occlusion report waits, preserving the hybrid write tracking and waiting before forwarded reads. The project lead reported that black flashing rocks in the tested cave disappeared.
- Bounded invalid texture-handle diagnostics remain in the source.

## Validation and limits

The reference was tested manually on an i9-12900F / RTX 4070 / 32 GB Windows system. Mario Kart improved substantially in the tested case; Zelda performance still varies and busy village views remain demanding. These are user observations, not standardized comparative benchmarks. No claim is made that every graphical issue is fixed or that every game is faster than upstream.

Existing local checks covered selective invalidation, page-filter transitions, report-filter scenarios and a limited JIT smoke test. They are not a comprehensive proof of emulation correctness.

Publication only adds documentation and removes a private AI-session link from local commit metadata. The runtime source tree is unchanged.

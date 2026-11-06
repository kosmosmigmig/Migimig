# Migimig

Migimig is an independent community integration fork of Lichii, based on Frizti v2 with selected upstream and local fixes. It builds on the work of Lichii, Eglantine, Eden, yuzu, Sudachi and their contributors. It is not an emulator written from scratch and is not affiliated with Nintendo or endorsed by the upstream authors.

The initial reference focuses on preserving rendering correctness while improving Ocarina of Time and Mario Kart World behaviour on Windows. Performance varies substantially by scene, hardware and driver. No universal 60 FPS claim is made.

## Project direction and implementation

An unnamed project lead directed the research, coordinated AI-assisted investigations, selected and evaluated changes, set visual-quality requirements, and carried out iterative testing and validation. Codex and Claude assisted with code analysis, adaptation, implementation and integration. AI assistance does not replace the original developers' authorship.

See **CREDITS-MIGIMIG.md** for provenance and **CHANGES-MIGIMIG.md** for the initial integration. Original copyright notices, license files and contributor history are retained.

## Initial release

The source is the validated MSVC reference, with publication documentation added. Rendering algorithms have not been changed for the rebrand. The initial executable, when distributed, retains the Lichii window title to avoid presenting an untested rebuild as the validated binary.

Games, keys, firmware, saves, shader caches and private diagnostics are not distributed. Keep user data outside installation/build directories. Do not delete an existing data directory or move saves merely to try this fork.

## Building

Use the upstream build documentation in docs and the dependency versions in cpmfile.json. The validated Windows build used MSVC, Ninja, Release mode and Qt 6.8.3 (msvc2022_64), with bundled Qt disabled. Optional updater, Discord presence, command-line and room targets were disabled. No claim is made that a different compiler produces identical behaviour.

## License

See LICENSE.txt, LICENSES and the original per-file notices. Existing license and attribution obligations apply to this derivative. Third-party dependencies retain their own licenses.

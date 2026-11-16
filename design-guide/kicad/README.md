# BenchPod test header (KiCad)

A 2x13, 2.54 mm test header for boards you want to test with a BenchPod. Its pin numbers match the
BenchPod LA cable (a 2x13 IDC socket wired straight through, ribbon wire n to pin n), so a cable from
the pod plugs straight into it. The design guide explains the pin assignment and the rules:
https://embeddedci.com/docs/design-for-benchpod

- `BenchPod_TestHeader.kicad_sym`: symbol, library nickname `BenchPod_TestHeader`
- `BenchPod_TestHeader.pretty/BenchPod_TestHeader_2x13_P2.54mm_Vertical.kicad_mod`: footprint (through hole, pin 1 square)

Add both to KiCad (Preferences, Manage Symbol Libraries and Manage Footprint Libraries) under the nickname
`BenchPod_TestHeader`. The symbol's pin names are a suggested assignment of the pod's LA channels; rename
them to your own signals. For a shrouded IDC box header, use the same footprint with a
2x13 2.54 mm box header part (for example the 2x13 right-angle or vertical box header you stock).

Pins 17 and 18 are the pod's own 3.3 V and 1.8 V rails: leave them unconnected on your board.

MIT, like the rest of this repository.

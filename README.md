# BenchPod

**NOTE1: Some tagged versions will have obvious mistakes in them, but as those got built, they're in the repo for historical reasons.**

**NOTE2: Don't build these boards yourself without any necessary changes. The current tagged versions are not production-ready yet.**

**An open hardware bench tool with sensor sim, CAN, analog I/O, and power control, with a Python SDK and pytest integration.**

Embedded teams often end up with a bench full of equipment that's hard to share, hard to automate, and difficult to use remotely. Setting up tests often means being physically present, and that doesn't scale well across a team.

BenchPod is an attempt to make that easier. One board with sensor simulation over I2C and SPI, CAN bus, analog input and output, programmable power control, a logic analyzer, and an FPGA for fast protocol mocking, connected over WiFi so it can be shared across a team or accessed remotely. A Python SDK and pytest integration make it straightforward to go from manual bench work to automated tests without changing your setup.

This repo contains the KiCad source files for the board, plus the SPICE simulations used while designing the analog front ends.

---

## What's in this repo

```
pcb/
  benchpod/                      # KiCad project for the analog + digital board
    vbench-pod.kicad_pro         #   KiCad project file
    vbench-pod.kicad_pcb         #   PCB layout
    vbench-pod.kicad_sch         #   Top-level schematic
    analog-power-v2.kicad_sch    #   Analog supply rails
    analog-switching.kicad_sch   #   Analog signal routing / muxing
    analog-to-digital-v2.kicad_sch  # ADC front end
    digital-to-analog-v2.kicad_sch  # DAC output stage
    LogicAnalyzer.kicad_sch      #   Logic analyzer
    power.kicad_sch              #   Power control
    ethernet.kicad_sch           #   Ethernet
    usb.kicad_sch                #   USB
    fp-lib-table                 #   Footprint library references
    sym-lib-table                #   Symbol library references
  benchpod-digital/              # KiCad project for the digital-only board (same sheet layout)
  libs/                          # Shared symbol, footprint, and 3D-model libraries

spice/                           # LTspice / ngspice simulations for the analog front ends
  adc-v1/  adc-v2/  dac-v2/
```

Library paths in `fp-lib-table`, `sym-lib-table`, and the PCB are stored relative to
the project (`${KIPRJMOD}/..`), so the project opens in KiCad straight after cloning.

---

## Which board do I have?

The board name is printed on the silkscreen (for example "BenchPod v3-r1"). Find it in the table
below to get the git tag with the exact design files for your board:

| Silkscreen | Board | Tag | KiCad project | What changed |
|---|---|---|---|---|
| BenchPod v3 | Analog + digital | `analog-v3` | `pcb/benchpod` | First v3 board. STM32H563ZIT6, INA238 current monitors. |
| BenchPod v3-Digital | Digital only | `digital-v3` | `pcb/benchpod-digital` | First digital-only board: the v3 without the analog section. STM32H563ZGT6 (1 MB flash), INA226 current monitors. |
| BenchPod v3-r1 | Analog + digital | `analog-v3r1` | `pcb/benchpod` | STM32H563ZGT6 and INA226 like the digital board. Monitors the pod's own current (INA226 at 0x41). The 5.5 V analog rail comes from a 7 V boost instead of the 14 V rail, so U50 no longer runs hot. TPS65131 compensation caps fixed. THS4551 and TPS7A2050 in their smaller packages (RUN, DQN). |
| BenchPod v3r2-Digital | Digital only | `digital-v3r2` | `pcb/benchpod-digital` | Monitors the pod's own current (INA226 at 0x41). |

To get the files for your board, check out its tag:

```
git checkout analog-v3r1
```

Every tag holds both KiCad projects; use the folder from the table. Older boards: `v1.0.0` and
`v1.0.1` are v1, `v2.0.0` is v2.

The v3 tags used to be named `v3.0.0` (now `analog-v3`), `v3.0.1-digital` (now `digital-v3`),
`v3.0.1-analog` (now `analog-v3r1`) and `v3.0.2-digital` (now `digital-v3r2`).

One firmware runs on all v3 boards. The pod's own current needs firmware newer than 3.5.1.

---

## License

Hardware (schematics, PCB layout) is released under [CERN OHL-W v2](https://ohwr.org/cern_ohl_w_v2.txt).

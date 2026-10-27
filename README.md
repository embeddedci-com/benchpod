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
| BenchPod v3-r2 | Analog + digital | `analog-v3r2` | `pcb/benchpod` | One DAC8554 quad DAC (a channel per output) replaces the DAC8551 and its two TMUX1104 muxes. The ±14 V supply starts off and the firmware switches it on. 0.1 % resistors around the ADC driver for a smaller zero offset between pods. Fixed 9.1 pF ADC compensation instead of the trimmer. SWD and USART2 on DNP 2x2 headers instead of H1-H3. More ESD clamps (USB CC, +1V8, LA_VCCIO, the 0-5 V SMA). Board revision strap 2.70 V. |
| BenchPod v3r3-Digital | Digital only | `digital-v3r3` | `pcb/benchpod-digital` | 24-pin FFC connector (CN1) for the analog module. The module 5 V and the USB-A bridge 5 V are switched by SY6280AAC power switches, with TVS diodes on the 5 V outputs. 3.3 V buck becomes a TPS62130A with a 2.2 uH inductor. PSRAM in SOP-8. Ethernet EMI changes from the Microchip and TI reference designs: RJ45 chassis ground straight to GND, center taps fed through a 0 ohm resistor, 8.2 pF on the four data lines, a flow-through TPD4E05U06 ESD clamp. 100 nF + 470 pF at the J4, J5 and J6 terminals. Connectors placed for the enclosure. |
| BenchPod v3-r3-analog | Analog module | `analog-v3r3` | `pcb/benchpod-analog` | First analog module: the analog section on its own board, connected to the v3r3 digital board by a 24-pin FFC (CN1). Front-panel connectors for the enclosure: a lead-free BNC for the ADC input (ready for 10x probes), pluggable terminal blocks for the DAC outputs (one 6-pin block) and the 4-20 mA loop. Module ID EEPROM. +3V3 from an AP2112K-3.3. |

To get the files for your board, check out its tag:

```
git checkout analog-v3r1
```

Every tag holds all KiCad projects; use the folder from the table. Older boards: `v1.0.0` and
`v1.0.1` are v1, `v2.0.0` is v2.

The v3 tags used to be named `v3.0.0` (now `analog-v3`), `v3.0.1-digital` (now `digital-v3`),
`v3.0.1-analog` (now `analog-v3r1`) and `v3.0.2-digital` (now `digital-v3r2`).

One firmware runs on all v3 boards. The pod's own current needs firmware newer than 3.5.1.
The v3-r2 board needs firmware newer than 3.9.4: older firmware runs it as a v3-r1 and its DAC
outputs and ±12 V stay off.

---

## License

Hardware (schematics, PCB layout) is released under [CERN OHL-W v2](https://ohwr.org/cern_ohl_w_v2.txt).

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
  benchpod/                      # KiCad project for the current board (v2)
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
  libs/                          # Shared symbol, footprint, and 3D-model libraries

spice/                           # LTspice / ngspice simulations for the analog front ends
  adc-v1/  adc-v2/  dac-v2/
```

Library paths in `fp-lib-table`, `sym-lib-table`, and the PCB are stored relative to
the project (`${KIPRJMOD}/..`), so the project opens in KiCad straight after cloning.

---

## License

Hardware (schematics, PCB layout) is released under [CERN OHL-W v2](https://ohwr.org/cern_ohl_w_v2.txt).

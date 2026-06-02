# BenchPod

**An open hardware bench tool with sensor sim, CAN, analog I/O, and power control, with a Python SDK and pytest integration.**

Embedded teams often end up with a bench full of equipment that's hard to share, hard to automate, and difficult to use remotely. Setting up tests often means being physically present, and that doesn't scale well across a team.

BenchPod is an attempt to make that easier. One board with sensor simulation over I2C and SPI, CAN bus, analog input and output, programmable power control, a logic analyzer, and an FPGA for fast protocol mocking, connected over WiFi so it can be shared across a team or accessed remotely. A Python SDK and pytest integration make it straightforward to go from manual bench work to automated tests without changing your setup.

This repo contains the KiCad source files.

---

## What's in this repo

```
pcb/vbench-pod/
  vbench-pod.kicad_pcb       # PCB layout
  vbench-pod.kicad_sch       # Top-level schematic
  vbench-pod.kicad_pro       # KiCad project file
  analogue.kicad_sch         # Analog frontend sub-sheet
  digital-to-analog.kicad_sch
  LogicAnalyzer.kicad_sch
  power.kicad_sch
  fp-lib-table               # Footprint library references
  sym-lib-table              # Symbol library references
```

---

## License

Hardware (schematics, PCB layout) is released under [CERN OHL-W v2](https://ohwr.org/cern_ohl_w_v2.txt).

# BenchPod v4 pogo fixture

A passive fixture for flashing and testing BenchPod v4 digital boards. The pod sits on top, and
eight spring probes touch the J10 test pads on the bottom of the pod.

The fixture is drawn in the same coordinates as `../benchpod-digital/vbench-pod.kicad_pcb`, so
every hole and probe lines up with the pod.

## Parts

| Ref | Part | Notes |
|---|---|---|
| J2 | 8 × P75 probes in R75 press-fit receptacles | 1.7 mm plated holes at 2.54 mm pitch, right under the pod's J10 |
| J1 | 1×8 right-angle pin header, 2.54 mm | Goes to the controller pod |
| H1, H2 | M2.5 × 8 mm hex standoffs, female-female | Under the pod's H11 and H14 (2.7 mm holes, 86.34 mm apart) |
| H3, H4 | M2.5 feet | Use 25 mm feet at all four holes so the receptacle tails clear the bench |

The 8 mm gap assumes the probe tips stand 10 mm above the fixture with nothing pressing on them,
which uses about 2 mm of probe travel. Check the free height in the probe datasheet before ordering
the standoffs.

## J1 pinout

| J1 | Net | Pod J10 pad | Pod signal |
|---|---|---|---|
| 1 | POD_5V | 1 | +5V_EFUSE (through the pod's input eFuse) |
| 2 | SWDIO | 3 | SWDIO |
| 3 | NRST | 5 | NRST |
| 4 | POD_TX | 7 | USART2_TX (the pod's console out) |
| 5 | POD_RX | 8 | USART2_RX |
| 6 | GND | 6 | GND |
| 7 | SWCLK | 4 | SWCLK |
| 8 | GND | 2 | GND |

## Using it

Wire J1 to a controller BenchPod. Use its target power for POD_5V, three LA channels for SWDIO,
SWCLK and NRST, and a UART receive channel on POD_TX. A test script then:

1. Turns target power on.
2. Waits for the boot banner on the UART.
3. Flashes the pod over SWD.
4. Reads the self-test result.
5. Turns target power off.

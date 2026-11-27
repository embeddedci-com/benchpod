# BenchPod v4 pogo fixture

A passive fixture for flashing and testing BenchPod v4 digital boards. The pod sits on top, and
eight spring probes touch two groups of test pads on the bottom of the pod:

- **J10** (6 pads, right of the STM32): SWD, NRST and the USART2 console.
- **J12** (2 pads, next to the input eFuse U57): 5 V and GND.

The 5 V pads sit next to U57 so the pod's power track stays short. The 5 V pad only has GND
next to it, so a short across neighboring pads reaches the supply's current limit, never an
STM32 pin.

The fixture is drawn in the same coordinates as `../benchpod-digital/vbench-pod.kicad_pcb`, so
every hole and probe lines up with the pod.

## Parts

| Ref | Part | Notes |
|---|---|---|
| J2 | 6 × P75 probes in R75 press-fit receptacles | 1.7 mm plated holes, 2.54 mm pitch, under the pod's J10 (pad 1 at 124.50, 83.54) |
| J3 | 2 × P75 probes in R75 press-fit receptacles | Under the pod's J12 (pad 1 at 119.50, 118.50) |
| J1 | 1×8 right-angle pin header, 2.54 mm | Goes to the controller pod; the pins hang over the bottom edge |
| H1, H2 | M2.5 × 8 mm hex standoffs, female-female | Under the pod's H11 and H14 (2.7 mm holes, 86.34 mm apart) |
| H3, H4 | M2.5 feet | Use 25 mm feet at all four holes so the receptacle tails clear the bench |

The 8 mm gap assumes the probe tips stand 10 mm above the fixture with nothing pressing on them,
which uses about 2 mm of probe travel. Check the free height in the probe datasheet before ordering
the standoffs.

## J1 pinout

| J1 | Net | Pod pad | Pod signal |
|---|---|---|---|
| 1 | GND | | GND |
| 2 | POD_RX | J10.6 | USART2_RX |
| 3 | SWDIO | J10.4 | SWDIO |
| 4 | SWCLK | J10.2 | SWCLK |
| 5 | GND | J10.1, J12.2 | GND |
| 6 | NRST | J10.3 | NRST |
| 7 | POD_TX | J10.5 | USART2_TX (the pod's console out) |
| 8 | POD_5V | J12.1 | +5V_EFUSE (before the pod's input eFuse) |

## Using it

Wire J1 to a controller BenchPod. Use its target power for POD_5V, three LA channels for SWDIO,
SWCLK and NRST, and a UART receive channel on POD_TX. A test script then:

1. Turns target power on.
2. Waits for the boot banner on the UART.
3. Flashes the pod over SWD.
4. Reads the self-test result.
5. Turns target power off.

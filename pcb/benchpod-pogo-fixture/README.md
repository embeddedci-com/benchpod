# BenchPod v4 pogo fixture

A passive fixture for flashing and testing BenchPod v4 digital boards. Eight SMD pogo pins touch two
groups of test pads on the bottom of the pod:

- **J10** (6 pads, right of the STM32): SWD, NRST and the USART2 console.
- **J12** (2 pads, next to the input eFuse U57): 5 V and GND.

The fixture board lies flat in a printed stand with a toggle clamp lever (benchpod-private,
`enclosure/pogo_fixture_stand.py`). Per pod: drop it on the four pins, push the lever down, flash,
lift the lever.

The board is drawn in the same coordinates as `../benchpod-digital/vbench-pod.kicad_pcb`, so every
hole and pin lines up with the pod.

## Parts

| Ref | Part | Notes |
|---|---|---|
| P1–P8 | BAT WIRELESS BWCD-L6.5W2.0H2.0, LCSC C2826552 | SMD pogo pin, 6.5 mm, 2.0 mm plunger out, 100 g; JLC reflows them. In the BOM and placement files. |
| J1 | 1×8 right-angle pin header, 2.54 mm | Goes to the controller pod; the pins hang over the bottom edge |
| H1, H2 | 6.4 mm holes | The stand's posts under the pod's H11/H14 come up through them |
| H3, H4 | M2.5 plated holes | M2.5×8 screws into the stand's floor |

The stand holds the pod 5.5 mm above the fixture board, which presses the pins 1.0 mm.

## Pin map

| Pin | Pod pad | Net | J1 |
|---|---|---|---|
| P1 | J10.1 | GND | 5 |
| P2 | J10.2 | SWCLK | 4 |
| P3 | J10.3 | NRST | 6 |
| P4 | J10.4 | SWDIO | 3 |
| P5 | J10.5 | USART2_TX (the pod's console out) | 7 |
| P6 | J10.6 | USART2_RX | 2 |
| P7 | J12.1 | +5V_EFUSE (before the pod's input eFuse) | 8 |
| P8 | J12.2 | GND | 5 |

J1: 1 GND, 2 POD_RX, 3 SWDIO, 4 SWCLK, 5 GND, 6 NRST, 7 POD_TX, 8 POD_5V.

## Using it

Wire J1 to a controller BenchPod. Use its target power for POD_5V, three LA channels for SWDIO,
SWCLK and NRST, and a UART receive channel on POD_TX. A loop on the controller then:

1. Keeps target power on, current-limited, and waits until the pod draws current.
2. Waits for the boot banner on the UART.
3. Flashes the pod over SWD.
4. Reads the self-test result and shows pass or fail.
5. Waits for the current to drop when the pod comes off.

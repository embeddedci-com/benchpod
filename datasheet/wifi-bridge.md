<!-- title: BenchPod Wi-Fi bridge datasheet -->
<!-- output: BenchPod-WiFi-bridge-datasheet.pdf -->
<!-- footer: BenchPod Wi-Fi bridge datasheet · Rev A · November 2026 · embeddedci.com -->

<div class="cover" markdown="1">
<div class="brand">EmbeddedCI</div>

# BenchPod Wi-Fi bridge

<div class="subtitle">Ethernet-to-Wi-Fi bridge accessory for BenchPod</div>
<div class="meta">Datasheet · Rev A · November 2026 · Board rev2 · US and Canada</div>
</div>

<div class="columns" markdown="1">
<div markdown="1">

### Overview

BenchPod has no radio. The Wi-Fi bridge gives it a Wi-Fi uplink: it plugs into the pod's ETHERNET port with a short patch cord and takes 5 V from the pod's BRIDGE POWER port. The pod reaches the network through the bridge as if it were wired.

The bridge forwards the pod's traffic at layer 2, using the pod's own MAC address on Wi-Fi. The router sees the pod itself, so DHCP, mDNS and the EmbeddedCI cloud connection work as on a cable. The bridge has no IP address and no open ports.

Everything is managed through the pod: Wi-Fi setup, status and firmware updates. There is nothing to configure on the bridge itself.

</div>
<div markdown="1">

### Key features

- **Radio**: pre-certified Espressif ESP32-WROOM-32E-N8 module, PCB antenna, 2.4 GHz Wi-Fi
- **Security**: WPA2 and WPA3 Personal; paired with one pod; Wi-Fi passphrase sent encrypted; signed firmware
- **Transparent**: layer-2 bridge for the pod's MAC only, no IP address, no open ports, no access point mode
- **Managed by the pod**: setup from the web app or the CLI, status in the pod's status
- **Safe updates**: through the pod, signed images, automatic rollback, factory image as a fallback
- **Power**: 5 V from the pod over USB-C, about 0.8 W idle
- **Small**: 70 x 52 mm board

</div>
</div>

<div class="keep" markdown="1">

### How it connects

```
 Wi-Fi access point )))  [ Wi-Fi bridge ]  ETHERNET ======= patch cord ======= ETHERNET  [ BenchPod ]
                                            POWER (USB-C) <-- USB-A to USB-C -- BRIDGE POWER (USB-A)
```

</div>

## Specifications

<div class="keep" markdown="1">

### Radio

| Parameter | Value |
|---|---|
| Module | Espressif ESP32-WROOM-32E-N8 (8 MB flash), PCB antenna |
| Standards | IEEE 802.11 b/g/n, 2.4 GHz |
| Channels | 1 to 11 (2412 to 2462 MHz), US country setting |
| Transmit power | The module's normal maximum, set by its calibration data; never raised by the firmware |
| Security | WPA2-Personal, WPA3-Personal (SAE), or an open network. No WEP or WPA1 |
| Bluetooth | Not used (off in the firmware) |
| Module approvals | FCC ID 2AC7Z-ESP32WROOM32E (single modular approval), ISED 21098-ESPWROOM32E |

</div>
<div class="keep" markdown="1">

### Network

| Parameter | Value |
|---|---|
| Ethernet | 10/100 Mbit/s, RJ45 with magnetics and link/activity LEDs (Microchip LAN8742A PHY) |
| Function | Layer-2 bridge for one device: the paired pod's MAC |
| Throughput (measured) | Pod to host 7.9 to 8.7 Mbit/s; host to pod 1.9 Mbit/s, limited by the pod's own network stack |
| Wi-Fi join | About 3 s |
| Back on the network after a bridge restart | About 10 s |

</div>
<div class="keep" markdown="1">

### Power

| Parameter | Value |
|---|---|
| Input | 5 V on USB-C (power only, no data), from the pod's BRIDGE POWER port |
| Joined, idle | 0.154 A (0.77 W) |
| Joined, 7.9 Mbit/s traffic | 0.200 A (1.0 W) |
| No pod for 30 s, Wi-Fi off | 0.061 A (0.31 W) |
| Supply margin | Keeps running under full traffic down to 3.6 V input (measured) |
| Regulator | TLV62569 buck, 5 V to 3.3 V |

</div>
<div class="keep" markdown="1">

### Mechanical

| Parameter | Value |
|---|---|
| Board | 70 x 52 mm, 1.6 mm, 4 layers |
| Mounting holes | 4x M2 (2.2 mm) |
| Supplied as | Bare board (plastic case planned) |
| Board revision | rev2, printed on the silkscreen |

</div>

## Ports and controls

| Name | Type | Use |
|---|---|---|
| ETHERNET | RJ45 | To the pod's ETHERNET port with the supplied patch cord |
| POWER | USB-C, power only | 5 V from the pod's BRIDGE POWER port with the supplied USB-A to USB-C cable |
| PAIR | Button, board edge | Forgets the paired pod; the next pod that connects is trusted |
| FACTORY | Button, board edge | Hold 5 s while running: clears the Wi-Fi settings. Hold 5 s while powering up: returns to the factory firmware and clears the pairing |
| Programming pads | Tag-Connect TC2030 | Factory programming and debug only, not a user port |

The board has no status LEDs. The RJ45 LEDs show the Ethernet link, and the pod reports the bridge's state in its status and in the web app's Settings.

## Getting started

<div class="keep" markdown="1">

1. Connect the bridge's ETHERNET to the pod's ETHERNET with the patch cord.
2. Connect the bridge's POWER to the pod's BRIDGE POWER with the USB-A to USB-C cable.
3. The pod pairs with the bridge by itself within a few seconds.
4. Set the Wi-Fi network from the web app (Settings), or from the CLI with the pod on USB:

```
benchpod set-wifi
```

The pod reports when the bridge has joined, or why it could not (network not found, wrong passphrase). Only the bridge stores the Wi-Fi settings.

</div>

## Security

- **Paired with one pod.** The first pod that connects is trusted. The pairing key is agreed with X25519 and never sent over the cable. The bridge only accepts signed, replay-protected requests from that pod (HMAC-SHA256), and only from the Ethernet side, never from Wi-Fi.
- **The Wi-Fi passphrase is never in the clear.** The pod sends it encrypted (XChaCha20). No command reads it back. Production units store it with ESP32 flash encryption.
- **Signed firmware only.** The bridge installs an image only with a valid signature from EmbeddedCI's release keys. Production units also use ESP32 secure boot.
- **Nothing to attack on the network.** The bridge has no IP address, no open ports and no access point mode. It forwards frames for the paired pod's MAC address only.

## Firmware updates and recovery

The pod updates the bridge automatically when a new bridge firmware comes with a pod firmware release. The bridge keeps two update slots plus a read-only factory image. A new image must prove itself by talking to the pod within 120 s, or the bridge returns to the previous image on its own.

If the bridge stops working:

1. Power-cycle it (unplug POWER, or restart the pod). A broken new image rolls back by itself.
2. Still not working: hold FACTORY, plug in POWER, keep holding 5 s, then release. The bridge starts its factory firmware with no Wi-Fi settings and no pairing.
3. The pod pairs again by itself and updates the bridge. Set the Wi-Fi network again.

## Usage notes

- **Keep at least 20 cm between the bridge and people.** This is a condition of the radio module's approval.
- **US and Canada only.** The bridge is not sold in the EU or the UK.
- **2.4 GHz networks only.** The bridge does not join 5 GHz networks, WPA2-Enterprise, or captive-portal networks.
- **Indoor use, short cables.** Use the supplied patch cord and USB cable, and keep the bridge next to the pod.
- **One pod per bridge.** Press PAIR to move the bridge to another pod.
- **Do not cover the antenna.** Keep metal away from the module's antenna end.

<div class="page-break"></div>

## Information for test labs

The bridge is tested mounted on BenchPod as shipped (configuration 2 of the BenchPod EMC test plan, a separate document). For testing, the bridge runs an EMC test firmware: from power-on it transmits continuously on channel 6 at 1 Mbit/s and the module's normal maximum power, without an access point, and carries the pod's test traffic on the air. Its debug console on the programming pads can change the channel, rate and power, and stop or start the transmitter.

<div class="keep" markdown="1">

### Port classification

| Port | Type | Notes |
|---|---|---|
| ETHERNET | Wired network port | 10/100 Mbit/s, to the pod only, supplied patch cord |
| POWER | DC power port (input) | 5 V on USB-C from the pod, supplied cable; no data |
| Antenna | Radio | Module PCB antenna, not removable |

There is no mains port: the bridge runs from the pod's 5 V output.

</div>
<div class="keep" markdown="1">

### Internal frequencies

| Source | Frequency |
|---|---|
| Wi-Fi radio | 2412 to 2462 MHz (channels 1 to 11) |
| ESP32 CPU | 240 MHz |
| ESP32 module crystal | 40 MHz |
| ESP32 module flash | 40 MHz |
| RMII reference oscillator | 50 MHz |
| TLV62569 buck | About 1.5 MHz switching |

</div>
<div class="keep" markdown="1">

### Radio module approvals

| Region | Identifier |
|---|---|
| US (FCC Part 15C, modular approval) | FCC ID 2AC7Z-ESP32WROOM32E, granted 2020-04-10 |
| Canada (ISED) | IC 21098-ESPWROOM32E |

Host labeling: "Contains FCC ID: 2AC7Z-ESP32WROOM32E" and "Contains IC: 21098-ESPWROOM32E". The module antenna and its power settings are used unchanged.

</div>

## Compliance

In progress, together with BenchPod: FCC Part 15B and ICES-003 Class B for the host, with a host-integration check of the radio module. Current status: [embeddedci.com/compliance](https://www.embeddedci.com/compliance).

<div class="small">

IN4IT LLC, d/b/a EmbeddedCI · hello@embeddedci.com · embeddedci.com. Specifications are subject to change without notice.

</div>

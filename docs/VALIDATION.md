# Validation record

Recorded November 18, 2026. These are observations from the original device, not results from a fresh public-guide installation.

| Item | Evidence / status |
|---|---|
| USB networking | Surface Duo USB045e:0c28, rndis_host, DHCP interface observed |
| Direct cable traffic | Established RDP TCP session between the two USB-subnet addresses on 3390 |
| Native Android rendering | Owner screenshots show Ubuntu in Windows App without browser chrome |
| Virtual display | Mutter reported Meta-0,1800x2700,2x scale |
| Built-in display | DSI-1,1280x720,59.901Hz retained |
| Full tall desktop | Owner confirmed extended display works |
| Trackball cursor | Owner confirmed visible after1x magnifier enabled |
| Primary/dock configuration | Applied through Mutter and GNOME settings; primary watcher active |
| Half-screen shortcuts | Registered in active Ubuntu Tiling Assistant 54; precise hinge fit not confirmed |
| Wi-Fi RDP restriction | Connection to the Wi-Fi address on 3390 rejected |
| 3MF artifact | ZIP integrity passes;1 mesh, millimeter units, no model metadata fields; SHA256 supplied |
| All-wireless-off test | Pending; direct USB route verified, but deliberate offline test not completed |
| New public-guide installation | Not run end-to-end; scripts derive from the working setup, with identifiers generalized |
| Reconnect/orientation endurance | Not completed |
| Physical dock fit/printability | Not evaluated |
| Latency/FPS/battery benchmarks | Not measured |

The current public scripts use only Python standard library plus system PyGObject for GNOME settings/D-Bus. Syntax and packaging checks are recorded at publication. NetworkManager enrollment and firewall changes need validation on each target. Do not infer hardware support from a repository check alone.

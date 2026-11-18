# Surface Duo as a wired Ubuntu display for a uConsole, with touch and the built-in trackball

I mounted a Surface Duo above a ClockworkPi uConsole and used it as a wired desktop display. The uConsole still runs the applications and handles its physical keyboard and trackball. The Duo runs Microsoft's Windows App as an RDP client and supplies touch input.

The connection is USB tethering, not HDMI or USB video. Android exposes a USB network adapter, Linux picks it up with rndis_host, and RDP runs directly across that local link. I verified an established connection between the two USB addresses on port 3390. The desktop path doesn't involve my home server, a browser, or Tailscale. I haven't completed a deliberate test with every wireless interface disabled, so I'm keeping that distinction in the validation notes.

The useful GNOME setting is:

```sh
gsettings set org.gnome.desktop.remote-desktop.rdp screen-share-mode extend
```

Instead of mirroring the uConsole's 1280x720 panel, GNOME creates a virtual monitor using the dimensions requested by the Android client. Mine negotiated 1800x2700 with 2x scaling. It is part of the existing Wayland desktop session, so the uConsole keyboard and trackball still control it. It isn't a separate remote-login session.

The Duo's two panels appear to Ubuntu as one tall monitor. I actually like that: an app can use the whole thing. For apps I want on just one panel, I added optional Ubuntu Tiling Assistant shortcuts: Ctrl+Alt+1 for the top half, Ctrl+Alt+2 for the bottom half, and Ctrl+Alt+0 to maximize across both. Those are work-area halves; they don't model the hinge, and exact hinge clearance still needs testing.

Two details mattered:

- GNOME initially left the top bar on the built-in display. A small D-Bus watcher makes the virtual monitor primary when it appears, and Ubuntu Dock's multi-monitor setting exposes the dock on both outputs.
- The physical trackball moved and clicked correctly, but its cursor was invisible remotely. Enabling GNOME's magnifier at 1.0x made the physical cursor visible without zooming the desktop. That's a working workaround on this setup, not a claim that I've fixed GNOME's cursor handling.

I kept RDP authentication and restricted port 3390 to loopback plus the enrolled USB interface. A NetworkManager dispatcher tracks the USB adapter using its vendor/product/serial/driver. Those identifiers aren't cryptographic authentication; the RDP password and certificate still matter.

Hardware/software tested: uConsole CM4, Ubuntu 26.04.1 ARM64, GNOME Wayland, GNOME Shell 50.1, GNOME Remote Desktop 50.2, Ubuntu Tiling Assistant 54, Surface Duo with a DUO-DE Treble Android build, and Windows App. The physical uConsole panel remains about 60 Hz. The virtual monitor reporting 60 Hz doesn't prove the stream delivers 60 FPS, and I haven't benchmarked latency or battery life.

Setup, configs, limitations, and the DUO_DOCK_V10.3mf model are here:
https://github.com/haKC-ai/haKCdevConsole

This is a working prototype with a documented setup, not a universal image. Reconnect/orientation endurance and exact hinge-aware placement are still on the test list.

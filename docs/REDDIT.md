                    ██████████                                      ·✦·
                    █▓       ░██                                           ✧
                    █▒        ██ T H E   P I N A C L E  O F  H A K C I N G   Q U A L I T Y
        █████████████░        █████████████████ ████████████ ████████████      ████████████
       ██         ███░        ███▓▒▒▒▒▒▒▒▒▒▒▒██ █▒▒▒▒▒▒▒▒▓████        █████████▓          ▒█
       ██  ✧      ███         ███▒▒▒▒▒▒▒▒▒▒▒▒▓██████████████▓        ███▓▒      ▒▓░       ▒█
       ██         ███        ░██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓██▓▒▒▒▒▒▒▒▒█▓        ███░       ░██░       ▒█
       ██         ███        ▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▒▒▒▒▒▒▒▓▒        ██  ▓        ██░  ◆   ▓█
       ██         ██▓        ███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▓▒▒▒▒▒▒▒▓▒       ██   █        ██░       ▓
       ██         ██▒        ██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▓▒      ██    █        ▓█████████
       ██     ★              ██▒▒▒▒▒▒▒▒█▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒   ▒███████ █░       ░▓        █
       ██         ░░         ██▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ ▓        ░█ ▓       ░▒       ░█
       ██         ██░       ░█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ █░        ▒ █                ░█
       ██   ·     ██        ▓█▒▒▒▒▒▒▒▒▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ █░        ▒ █░               ▒█
        ██████████  ███████████▓██▓▓█▓█  █▓▒▒▒▒▒▒▒▒▒▓██▓██   █▓▓▓▓▓▓▓█    █▓▓▓▓▓▓/\▓▓▓▓▓▓██ 
      .:/____________________ █▓██▓██ ________ ████▓█▓████ _ ________________.  /  \.______\:.
         _ __ _______________  ██▓██ __________ █▓▓▓██ ██ __________________. \/ /\.____ ___
                                 █▓█             ██▓██                       \  /
                                  ██               ███                        \/
    
    NAME............................................haKCdevConsole
    Collective.............................................haKC.ai
    Host.............................uConsole CM4 / Ubuntu 26.04.1
    Display............................Surface Duo / DUO-DE Treble
    Link....................................USB tether > RDP :3390
    Size.......................................2 SCREENS / 1 CABLE
    Dock..........................................DUO_DOCK_V10.3mf
    Supplied by......................................../dev/CØR.23
    Release date..............................................1994
    
    GROUP NEWS: Dual screens on a uConsole. No HDMI. No dongles.
                No cloud. One USB cable and a Duo from the drawer.
    
    NFO:  Duo bolts on top, RDPs back over USB tether, and GNOME
          treats it as a real second monitor. Touch included.
    
    GR33TZ: SecKC, LEGACY CoWTownComputerCongress, ClockworkPi
            crew, DUO-DE, ACiD, iCE, badge lords
    
    SHOUTZ:
            [*] everyone with a Duo in a drawer "just in case"
            [*] l33t soulz still runnin' 720p on a 5" panel.
                help has arrived.
    
            FU to [LAMERZ] mirroring their screen instead of
            extending it.
    
               ───── ▓ signed, /dev/CØR.23 ▓ ─────
                    "two screens > one. come fight us."

720p on a uConsole is cozy until you need a terminal and docs open at the same time. So I bolted a Surface Duo to the top of it.

**How it works.** No HDMI and no USB video. The Duo turns on USB tethering, the uConsole sees it as a network card (`rndis_host`), and Windows App on the Duo RDPs straight across the cable. No cloud, no relay, no Tailscale. Just two USB addresses talking on 3390.

The trick is one line:

    gsettings set org.gnome.desktop.remote-desktop.rdp screen-share-mode extend

Instead of mirroring, GNOME spawns a virtual monitor sized to the Duo (1800x2700 @ 2x) inside the same Wayland session. It's a real second monitor, not a remote login. The keyboard and trackball drive it, and you get touch on the Duo for free.

**What else is in the repo**

- Both panels act as one tall screen. Ctrl+Alt+1 sends a window to the top half, Ctrl+Alt+2 to the bottom, Ctrl+Alt+0 to both.
- A D-Bus watcher moves the top bar over when the Duo connects, and the dock runs on both screens.
- The trackball cursor was invisible on the Duo. GNOME magnifier at 1.0x fixes it. Don't ask, it works.
- RDP is locked to loopback plus the enrolled USB interface, and auth stays on. (USB IDs aren't crypto. The password still matters.)

**The dock.** DUO_DOCK_V10.3mf bolts onto the uConsole screen area with 4x M4x8 countersunk screws. The bottom half of the Duo slides in and clicks into place, and the top half opens like a laptop. It prints flat with no supports. Mine is PETG on an AD5M.

**Tested on:** uConsole CM4, Ubuntu 26.04.1 ARM64, GNOME 50.1, GNOME Remote Desktop 50.2, Tiling Assistant 54, Duo 1 on a DUO-DE Treble build.

**Not tested yet:** an air-gapped run with every radio off, real FPS (60 Hz reported isn't 60 FPS delivered), latency, battery, long-session reconnects, hinge-aware window placement.

It's a prototype with real docs, not a flash-and-go image. Clone it, break it, send PRs.

https://github.com/haKC-ai/haKCdevConsole

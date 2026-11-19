# Setup

Run Linux commands on the uConsole, in its existing graphical login session. Android steps happen on the Duo. These instructions target the tested GNOME/NetworkManager system; do not replace a working desktop or upgrade the OS just to follow them.

## 1. Establish the cable connection

Use the uConsole USB host/data port and a data-capable cable to the Duo. On Android enable USB tethering in USB preferences or Network & internet > Hotspot & tethering. The tested device used rndis_host. The uConsole charging connector alone is not a substitute for a host data port.

Inspect:

```sh
lsusb
nmcli device
ip -brief address
ip route
```

Record the USB interface name and its IPv4 address as USB_IFACE and USB_IP. Do not use the Wi-Fi address or assume another person's DHCP address. Android may change the subnet/address after reconnect. USB tethering can also install an internet default route; this is not required for local RDP. Keep existing management connectivity until you verify the cable path.

## 2. Prerequisites and desktop sharing

Check installed packages and use your distribution's signed packages for missing components:

```sh
sudo apt install gnome-remote-desktop python3-gi nftables avahi-utils avahi-daemon
```

Ubuntu Tiling Assistant is optional but required for this repository's half-screen bindings. On Ubuntu the package is gnome-shell-extension-tiling-assistant. Validate extension compatibility with your GNOME version and confirm it is ACTIVE using gnome-extensions info tiling-assistant@ubuntu.com.

Before enabling RDP, install the USB guard below. If you already have an inet uconsole_remote table or uconsole-rdp-guard.service from this project, inspect and update that installation instead of installing a second guard.

## 3. Enroll the USB adapter and install the guard

From this repository root:

```sh
sudo python3 scripts/enroll-usb.py USB_IFACE
sudo install -m644 config/uconsole-rdp-guard.nft /etc/uconsole-rdp-guard.nft
sudo install -m755 scripts/90-uconsole-usb-rdp /etc/NetworkManager/dispatcher.d/90-uconsole-usb-rdp
sudo install -m644 config/uconsole-rdp-guard.service /etc/systemd/system/uconsole-rdp-guard.service
sudo install -m644 config/uconsole-usb-name.service /etc/systemd/system/uconsole-usb-name.service
sudo systemctl enable --now avahi-daemon.service
sudo systemctl daemon-reload
sudo systemctl enable --now uconsole-rdp-guard.service
sudo nft list table inet uconsole_remote
```

Replace USB_IFACE in the first command with the actual interface name. Enrollment stores vendor/product/serial/driver in a root-only local JSON file. The dispatcher updates a set of matching interfaces on network events. The rule accepts port 3390 on that set and loopback, rejects it on other interfaces, and does not flush other firewall tables. Other firewall chains may impose additional restrictions; an accept here does not override every later chain.

The file is an initial-boot ruleset. Do not repeatedly reload it into an already populated table. Review nftables changes before modifying an existing policy. If NetworkManager recreates an interface after boot, the dispatcher refreshes the set.

## 4. Configure GNOME Desktop Sharing

Open Ubuntu Settings > System > Remote Desktop > Desktop Sharing. Enable desktop sharing and remote control. Use Desktop Sharing for the already logged-in session, not Remote Login, which starts a different session. Set a dedicated username/password and note the certificate fingerprint. Desktop-sharing credentials are separate from the Linux login account.

Use the standard GNOME settings interface to create certificates and credentials. Do not copy someone else's certificate, password, or private environment file. A locked login keyring after automatic login can require manual unlocking; this public guide does not bypass it or ship internal credential-override environment variables.

Then configure the listener and virtual display:

```sh
grdctl rdp set-port 3390
grdctl rdp disable-port-negotiation
grdctl rdp disable-view-only
gsettings set org.gnome.desktop.remote-desktop.rdp screen-share-mode extend
systemctl --user restart gnome-remote-desktop
grdctl status
```

Expected: enabled RDP on 3390, view-only no. Do not use status --show-credentials in shared logs. Authentication and TLS must remain configured.

## 5. Connect from Android

Install Microsoft Windows App from the official Play Store listing:
https://play.google.com/store/apps/details?id=com.microsoft.rdc.androidx

Add a PC:

- PC name: uconsole-usb.local:3390. If the Android client cannot resolve mDNS, use USB_IP:3390 with the current uConsole USB address.
- Account: the desktop-sharing credentials configured above. Save them locally if desired.
- Gateway: none.
- Admin mode: off.

When asked about the self-signed certificate, compare its fingerprint with grdctl status on the uConsole before trusting it. Do not accept an unexplained certificate change. Connect with the Android app occupying the intended Duo display area. Spanning and orientation behavior depends on the Android build and app; the tested client negotiated1800x2700 when spanning the panels vertically. RDP cannot make Android span an app by itself.

Use the app's touch controls and verify the uConsole physical keyboard and trackball also operate the focused window. There is no browser chrome. Android may still show its own navigation or RDP toolbar.

## 6. Put the top bar and dock on Android

```sh
mkdir -p ~/.local/share/hakcdevconsole ~/.config/systemd/user
install -m644 scripts/primary-remote.py ~/.local/share/hakcdevconsole/primary-remote.py
install -m644 config/uconsole-remote-primary.service ~/.config/systemd/user/uconsole-remote-primary.service
systemctl --user daemon-reload
systemctl --user enable --now uconsole-remote-primary.service
gsettings set org.gnome.shell.extensions.dash-to-dock multi-monitor true
```

The watcher listens for Mutter monitor changes. While one virtual remote monitor exists, it makes that monitor the only active display at origin 0,0. When it disappears, it restores the built-in panel. Current scale and mode are preserved where available. Multiple virtual monitors are left unchanged. This uses the existing login session. Both transitions were verified on the tested device.

## 7. Visible physical trackball cursor

In the tested setup the physical trackball controlled windows but its pointer was invisible on Android. GNOME's existing magnifier at 1x provided a visible composited pointer:

```sh
gsettings set org.gnome.desktop.a11y.magnifier mag-factor 1.0
gsettings set org.gnome.desktop.a11y.applications screen-magnifier-enabled true
```

This is a workaround, not a claimed GNOME bug fix. It does not enlarge the desktop. The owner confirmed the physical cursor became visible. Test motion, touch and performance on your version; see rollback if unwanted.

## 8. Optional panel-like snapping

```sh
python3 scripts/configure-duo-snapping.py
```

Focus an app on the remote monitor:

| Shortcut | Action |
|---|---|
| Ctrl+Alt+1 | Top half |
| Ctrl+Alt+2 | Bottom half |
| Ctrl+Alt+0 | Maximize across the entire monitor |

Existing bindings are preserved. Native fullscreen remains available. These are work-area halves, not two monitors and not a hinge-aware layout engine. Test the hinge boundary, top bar, dock and application minimum sizes. No promise of exact physical-panel fit is made.

Optional show-desktop shortcut, after checking your existing binding:

```sh
gsettings get org.gnome.desktop.wm.keybindings show-desktop
gsettings set org.gnome.desktop.wm.keybindings show-desktop "['<Control><Alt>d']"
```

## 9. Verify independence

First verify the live connection is using USB:

```sh
ss -tn state established sport = :3390
ip route get ANDROID_USB_IP
```

The local address should be USB_IP:3390 and peer should be Android's USB address, routed through the USB interface. Once you have physical access and a working session, test without Wi-Fi/cellular on both devices, keeping USB tethering enabled. This deliberate offline test was not completed in the recorded session. Some Android builds couple tethering availability to other network state; do not assume all builds work identically.

## 10. Reconnect

Reconnect the data cable, re-enable USB tethering if required, and open the saved uconsole-usb.local connection. The dispatcher republishes the enrolled USB address after DHCP changes and withdraws the name when no unique address exists. Android hostname resolution still needs verification on each client; use the current USB IP if resolution fails. Verify primary display, pointer and snapping. The private-home-network viewer is a different path and is not needed for this USB setup.

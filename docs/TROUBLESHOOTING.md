# Troubleshooting and rollback

## PC cannot be found

Check the USB IPv4 address with ip -brief address. A single mistyped final octet caused the original 0x104 error. Use that address followed by:3390. Do not use the Android gateway address, a Wi-Fi address, a URL prefix, or a hostname that depends on the home DNS server. Keep Gateway=None and Admin mode=off.

Check USB tethering remains enabled, the interface has an address, the enrolled device matches, the firewall set contains its interface, and grdctl status reports port 3390. If Android uses a VPN, investigate whether it routes local USB destinations into the VPN. Do not broadly open the firewall as a workaround.

## Desktop works but is letterboxed

Confirm screen-share-mode=extend and reconnect. Check Mutter GetCurrentState. If it is still1280x720, the client may be requesting that size. Android app spanning and orientation must be configured on Android. Do not change the physical panel resolution to compensate.

## Wallpaper but no apps/top bar

Verify uconsole-remote-primary.service is active and the virtual monitor is primary. Ubuntu Dock multi-monitor should be true. Apps remain in the same session; a previously open window may still be on the built-in monitor. Move it to the virtual output, then use the half-screen shortcuts.

## Invisible physical trackball cursor

Check the 1x magnifier settings and distinguish physical-pointer visibility from the Android client's own pointer. If the workaround causes visual artifacts or performance trouble, disable it rather than claiming it fixed your configuration:

```sh
gsettings set org.gnome.desktop.a11y.applications screen-magnifier-enabled false
```

Restore any prior magnifier factor/accessibility settings you recorded. The original setup had factor2.0 and magnifier disabled; those are not necessarily your previous settings.

## Undo optional window shortcuts

Remove only the bindings added by this project, leaving pre-existing shortcuts intact:

```sh
python3 - <<'PYCODE'
from gi.repository import Gio
s=Gio.Settings.new('org.gnome.shell.extensions.tiling-assistant')
for key,value in [('tile-top-half','<Control><Alt>1'),('tile-bottom-half','<Control><Alt>2'),('tile-maximize','<Control><Alt>0')]:
    s.set_strv(key,[x for x in s.get_strv(key) if x != value])
Gio.Settings.sync()
PYCODE
```

## Return to physical-screen mirroring

```sh
systemctl --user disable --now uconsole-remote-primary.service
gsettings set org.gnome.desktop.remote-desktop.rdp screen-share-mode mirror-primary
systemctl --user restart gnome-remote-desktop
```

This disconnects the current RDP client. Reconnect afterward. Restore your previous dock preference separately.

## Remove USB access without exposing Wi-Fi

Disable the USB dispatcher first, then empty only its nftables set. Leave the reject rule installed:

```sh
sudo chmod -x /etc/NetworkManager/dispatcher.d/90-uconsole-usb-rdp
sudo nft flush set inet uconsole_remote usb_interfaces
```

Deleting the whole guard table while RDP listens would remove this protection. To retire desktop sharing completely, disable the RDP backend first with grdctl rdp disable, then review removal of this project's service/rules while preserving other firewall policy.

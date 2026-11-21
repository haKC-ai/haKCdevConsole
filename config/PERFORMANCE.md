# Performance settings

As the GNOME desktop user, apply `dconf load / < config/desktop-performance.ini`. This changes only the listed keys. Save prior values with `dconf dump / > desktop-before.ini` if rollback is needed; restore with `dconf load / < desktop-before.ini`.

`android-rdp-performance.json` is a settings reference, not an import file. Enable hardware acceleration under Windows App Profile > Display. Edit the saved PC > Customize display resolution: 1352 x 900, 100% scaling. Save, acknowledge the notice, disconnect and reconnect. The connection-specific setting overrides global resolution. Portrait negotiates 900 x 1352.

Turn Android adaptive brightness off in Display settings. With authorized USB ADB, the equivalent is `adb shell settings put system screen_brightness_mode 0`. Re-enable USB tethering after cable changes if needed.

Optional radio settings: Gqrx FFT rate 5; `cgps -s localhost:2947` for a compact GPS view. Neither setting enables radio transmission.

The remote monitor's 60 Hz mode does not establish streaming FPS. These settings do not enable server-side H.264 or Vulkan support.

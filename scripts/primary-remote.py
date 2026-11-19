"""Use Android exclusively during RDP; restore the built-in panel afterward."""
from gi.repository import Gio, GLib

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
proxy = Gio.DBusProxy.new_sync(bus, 0, None, 'org.gnome.Mutter.DisplayConfig',
    '/org/gnome/Mutter/DisplayConfig', 'org.gnome.Mutter.DisplayConfig', None)


def apply_primary():
    serial, monitors, logical, props = proxy.call_sync(
        'GetCurrentState', None, 0, -1, None).unpack()
    remote = [m for m in monitors if m[0][2] == 'Virtual remote monitor']
    if len(remote) > 1:
        return  # Do not guess which remote client owns the display.
    targets = remote or [m for m in monitors if m[2].get('is-builtin')]
    if len(targets) != 1:
        return
    monitor = targets[0]
    connector = monitor[0][0]
    active = next((l for l in logical if any(s[0] == connector for s in l[5])), None)
    if len(logical) == 1 and active and active[:2] == (0, 0) and active[4]:
        return
    mode = next((m for m in monitor[1] if m[6].get('is-current')), None)
    if mode is None:
        mode = next(m for m in monitor[1] if m[6].get('is-preferred'))
    scale, transform = (active[2], active[3]) if active else (mode[4], 0)
    config = [(0, 0, scale, transform, True, [(connector, mode[0], {})])]
    proxy.call_sync('ApplyMonitorsConfig', GLib.Variant(
        '(uua(iiduba(ssa{sv}))a{sv})', (serial, 1, config, {})), 0, -1, None)
    print('Only active display:', connector, flush=True)


def refresh():
    try:
        apply_primary()
    except (GLib.Error, StopIteration) as error:
        print('Display update failed:', error, flush=True)
    return False


if __name__ == '__main__':
    refresh()
    if '--watch' in __import__('sys').argv:
        def changed(proxy, sender, signal, parameters):
            if signal == 'MonitorsChanged':
                GLib.idle_add(refresh)
        proxy.connect('g-signal', changed)
        GLib.MainLoop().run()

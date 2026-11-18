from gi.repository import Gio, GLib
bus=Gio.bus_get_sync(Gio.BusType.SESSION,None)
proxy=Gio.DBusProxy.new_sync(bus,0,None,'org.gnome.Mutter.DisplayConfig','/org/gnome/Mutter/DisplayConfig','org.gnome.Mutter.DisplayConfig',None)
def apply_primary():
    serial,monitors,logical,props=proxy.call_sync('GetCurrentState',None,0,-1,None).unpack()
    virtual=[m[0][0] for m in monitors if m[0][2]=='Virtual remote monitor']
    if len(virtual)!=1: return
    if any(primary and any(spec[0]==virtual[0] for spec in specs) for x,y,scale,transform,primary,specs,properties in logical): return
    modes={m[0][0]:next(mode[0] for mode in m[1] if mode[6].get('is-current')) for m in monitors}
    config=[]
    for x,y,scale,transform,primary,specs,properties in logical:
     config.append((x,y,scale,transform,any(s[0]==virtual[0] for s in specs),[(s[0],modes[s[0]],{}) for s in specs]))
    proxy.call_sync('ApplyMonitorsConfig',GLib.Variant('(uua(iiduba(ssa{sv}))a{sv})',(serial,1,config,{})),0,-1,None)
    print('Primary display:',virtual[0])

apply_primary()
if '--watch' in __import__('sys').argv:
    def changed(proxy, sender, signal, parameters):
        if signal == 'MonitorsChanged':
            GLib.idle_add(refresh)
    def refresh():
        try: apply_primary()
        except GLib.Error as error: print(error, flush=True)
        return False
    proxy.connect('g-signal', changed)
    GLib.MainLoop().run()

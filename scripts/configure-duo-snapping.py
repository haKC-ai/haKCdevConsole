from gi.repository import Gio
settings=Gio.Settings.new('org.gnome.shell.extensions.tiling-assistant')
for key, shortcut in [('tile-top-half','<Control><Alt>1'),('tile-bottom-half','<Control><Alt>2'),('tile-maximize','<Control><Alt>0')]:
    current=settings.get_strv(key)
    if shortcut not in current: settings.set_strv(key,current+[shortcut])
    print(key,settings.get_strv(key))
Gio.Settings.sync()

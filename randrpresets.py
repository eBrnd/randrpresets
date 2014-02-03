#!/usr/bin/python
from gi.repository import Gtk

class RandrPresetsWindow(Gtk.Window):

  def __init__(self):
    Gtk.Window.__init__(self, title="RandRpresets")

    self.set_border_width(10)
    self.set_default_size(200, 200)

    hbox = Gtk.Box(spacing=6)
    self.add(hbox)

    listbox = Gtk.ListBox()
    listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    hbox.pack_start(listbox, True, True, 0)

    # XXX this will be done in a loop later
    row = Gtk.ListBoxRow()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
    row.add(hbox)

    # XXX this will be loaded from the "preset" object
    activate_button = Gtk.Button(label="Preset 1")
    hbox.pack_start(activate_button, True, True, 0)
    display_a_check_button = Gtk.CheckButton(label="eDP1")
    hbox.pack_start(display_a_check_button, True, True, 0)
    display_b_check_button = Gtk.CheckButton(label="VGA1")
    hbox.pack_start(display_b_check_button, True, True, 0)
    display_c_check_button = Gtk.CheckButton(label="HDMI1")
    hbox.pack_start(display_c_check_button, True, True, 0)

    listbox.add(row)

    # XXX another iteration...
    row = Gtk.ListBoxRow()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
    row.add(hbox)

    # XXX this will be loaded from the "preset" object
    activate_button = Gtk.Button(label="Preset 2")
    hbox.pack_start(activate_button, True, True, 0)
    display_a_check_button = Gtk.CheckButton(label="eDP1")
    hbox.pack_start(display_a_check_button, True, True, 0)
    display_b_check_button = Gtk.CheckButton(label="VGA1")
    hbox.pack_start(display_b_check_button, True, True, 0)
    display_c_check_button = Gtk.CheckButton(label="HDMI1")
    hbox.pack_start(display_c_check_button, True, True, 0)

    listbox.add(row)

win = RandrPresetsWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

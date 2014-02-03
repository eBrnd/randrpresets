#!/usr/bin/python
from gi.repository import Gtk

class RandrPresetsWindow(Gtk.Window):

  def __init__(self, presets):
    Gtk.Window.__init__(self, title="RandRpresets")

    self.presets = presets

    self.set_border_width(10)
    self.set_default_size(200, 200)

    hbox = Gtk.Box(spacing=6)
    self.add(hbox)

    listbox = Gtk.ListBox()
    listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    hbox.pack_start(listbox, True, True, 0)

    for preset in self.presets:
      row = Gtk.ListBoxRow()
      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
      row.add(hbox)

      activate_button = Gtk.Button(label=preset.name)
      hbox.pack_start(activate_button, True, True, 0)
      for screen in preset.screens:
        screen_check_button = Gtk.CheckButton(label=screen[0])
        screen_check_button.set_active(screen[1])
        hbox.pack_start(screen_check_button, True, True, 0)

      listbox.add(row)

class Preset:
  def __init__(self, name, screens=[]):
    self.name = name
    self.screens = screens

preset_a = Preset("Only internal", [["eDP1", True], ["VGA1", False], ["HDMI1", False]])
preset_b = Preset("Internal+VGA", [["eDP1", True], ["VGA1", True], ["HDMI1", False]])
preset_c = Preset("Internal+HDMI", [["eDP1", True], ["VGA1", False], ["HDMI1", True]])
presets = [preset_a, preset_b, preset_c]
win = RandrPresetsWindow(presets)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

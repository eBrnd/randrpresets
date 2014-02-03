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

    for preset_index in range(len(self.presets)):
      preset = presets[preset_index]
      row = Gtk.ListBoxRow()
      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
      row.add(hbox)

      activate_button = Gtk.Button(label=preset.name)
      hbox.pack_start(activate_button, True, True, 0)
      activate_button.connect("clicked", self.activate_button_clicked, preset_index)
      for screen_index in range(len(preset.screens)):
        screen = preset.screens[screen_index]
        screen_check_button = Gtk.CheckButton(label=screen[0])
        screen_check_button.set_active(screen[1])
        screen_check_button.connect("clicked", self.screen_button_clicked, preset_index, screen_index)
        hbox.pack_start(screen_check_button, True, True, 0)

      listbox.add(row)

  def activate_button_clicked(self, widget, button_id):
    print(presets[button_id].command())

  def screen_button_clicked(self, widget, preset_id, screen_id):
    presets[preset_id].screens[screen_id][1] = widget.get_active()

class Preset:
  def __init__(self, name, screens=[]):
    self.name = name
    self.screens = screens

  def command(self):
    res = 'xrandr'
    for screen in self.screens:
      res = res + ' --output ' + screen[0]
      if screen[1]:
        res = res + " --auto"
      else:
        res = res + " --off"

    return res

preset_a = Preset("Only internal", [["eDP1", True], ["VGA1", False], ["HDMI1", False]])
preset_b = Preset("Internal+VGA", [["eDP1", True], ["VGA1", True], ["HDMI1", False]])
preset_c = Preset("Internal+HDMI", [["eDP1", True], ["VGA1", False], ["HDMI1", True]])
presets = [preset_a, preset_b, preset_c]
win = RandrPresetsWindow(presets)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

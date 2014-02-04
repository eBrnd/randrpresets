#!/usr/bin/python
import os
from gi.repository import Gtk, Gio
import json

class RandrPresetsWindow(Gtk.Window):

  def __init__(self, presets, post_command):
    Gtk.Window.__init__(self, title="RandRpresets")

    self.post_command = post_command
    self.presets = presets

    self.set_border_width(10)
    self.set_default_size(200, 200)

    hb = Gtk.HeaderBar()
    hb.props.show_close_button = True
    hb.props.title = "RandRpresets"
    button = Gtk.Button()
    image = Gtk.Image.new_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.BUTTON)
    button.add(image)
    button.connect("clicked", self.save_button_clicked)
    hb.pack_end(button)

    self.set_titlebar(hb)

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
    os.system(presets[button_id].command())
    os.system(post_command)
    Gtk.main_quit()

  def screen_button_clicked(self, widget, preset_id, screen_id):
    self.presets[preset_id].screens[screen_id][1] = widget.get_active()

  def save_button_clicked(self, widget):
    preset_list = []
    for preset in self.presets:
      preset_list.append([preset.name, preset.screens])
    configstring = json.dumps({ "presets" : preset_list, "post_command" : self.post_command })
    with open(configfilename, 'w') as configfile:
      configfile.write(configstring)
    configfile.close()

class Preset:
  def __init__(self, name, screens=[]):
    self.name = name
    self.screens = screens

  def command(self):
    res = 'xrandr'
    prev_monitor = ""
    for screen in self.screens:
      res = res + ' --output ' + screen[0]
      if screen[1]:
        res = res + " --auto"
        if prev_monitor:
          res = res + " --right of " + prev_monitor
        prev_monitor = screen[0]
      else:
        res = res + " --off"

    return res


configfilename = os.environ["HOME"] + "/" + ".randrpresets.json"
with open(configfilename, 'r') as configfile:
  config = configfile.read()
  configdic = json.loads(config)
presets = configdic["presets"]
post_command = configdic["post_command"]

preset_list = []
for preset in presets:
  preset_list.append(Preset(preset[0], preset[1]))

win = RandrPresetsWindow(preset_list, post_command)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

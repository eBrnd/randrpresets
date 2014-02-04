#!/usr/bin/python
import os
import subprocess
from gi.repository import Gtk, Gio
import json

class RandrPresetsWindow(Gtk.Window):

  def __init__(self, presets, post_command):
    Gtk.Window.__init__(self, title="RandRpresets")

    self.post_command = post_command
    self.presets = presets

    self.set_border_width(10)
    self.set_default_size(200, 200)

    self.headerbar = Gtk.HeaderBar()
    self.headerbar.props.show_close_button = True
    self.headerbar.props.title = "RandRpresets"
    button = Gtk.Button()
    button.add(Gtk.Image.new_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.BUTTON))
    button.connect("clicked", self.save_button_clicked)
    self.headerbar.pack_end(button)

    button = Gtk.Button()
    button.add(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.BUTTON))
    button.connect("clicked", self.edit_post_command_button_clicked)
    self.headerbar.pack_end(button)

    button = Gtk.Button()
    button.add(Gtk.Image.new_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.BUTTON))
    button.connect("clicked", self.add_button_clicked)
    self.headerbar.pack_end(button)

    self.set_titlebar(self.headerbar)

    hbox = Gtk.Box(spacing=6)
    self.add(hbox)

    self.listbox = Gtk.ListBox()
    self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    hbox.pack_start(self.listbox, True, True, 0)

    for preset_index in range(len(self.presets)):
      row = self.make_listbox_row(preset_index)
      self.listbox.add(row)

  def activate_button_clicked(self, widget, button_id):
    os.system(self.presets[button_id].command())
    os.system(post_command)
    Gtk.main_quit()

  def screen_button_clicked(self, widget, preset_id, screen_id):
    self.presets[preset_id].screens[screen_id] = widget.get_active()

  def save_button_clicked(self, widget):
    preset_list = []
    for preset in self.presets:
      preset_list.append([preset.name, preset.screens])
    configstring = json.dumps({ "presets" : preset_list, "post_command" : self.post_command,
                                "screens" : available_screens },
                              indent=2, separators=(',', ': '))
    with open(configfilename, 'w') as configfile:
      configfile.write(configstring)
    configfile.close()

  def edit_post_command_button_clicked(self, widget):
    dialog = EditPostCommandDialog(self, self.post_command)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      self.post_command = dialog.get_text()
    dialog.destroy()

  def add_button_clicked(self, widget):
    preset = Preset("New Preset", [False]*len(available_screens))
    self.presets.append(preset)
    row = self.make_listbox_row(len(self.presets)-1)
    self.listbox.add(row)
    self.show_all()

  def delete_button_clicked(self, widget, preset_index):
    del self.presets[preset_index]
    # TODO is there a more elegant way than to recreate the whole list?
    for child in self.listbox.get_children():
      self.listbox.remove(child)
    for preset_index in range(len(self.presets)):
      row = self.make_listbox_row(preset_index)
      self.listbox.add(row)
    self.show_all()

  def make_listbox_row(self, preset_index):
    row = Gtk.ListBoxRow()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
    row.add(hbox)
    activate_button = Gtk.Button(label=self.presets[preset_index].name)
    hbox.pack_start(activate_button, True, True, 0)
    for screen_index in range(len(available_screens)):
      screen_name = available_screens[screen_index]
      screen_check_button = Gtk.CheckButton(label=screen_name)
      screen_check_button.set_active(self.presets[preset_index].screens[screen_index])
      screen_check_button.connect("clicked", self.screen_button_clicked, preset_index, screen_index)
      hbox.pack_start(screen_check_button, True, True, 0)

    button = Gtk.Button()
    button.add(Gtk.Image.new_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.BUTTON))
    button.connect("clicked", self.delete_button_clicked, preset_index)
    hbox.pack_start(button, True, True, 0)

    return row



class EditPostCommandDialog(Gtk.Dialog):
  def __init__(self, parent, existing_post_command):
    Gtk.Dialog.__init__(self, "Edit Post-Command", parent, 0,
                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
    label = Gtk.Label("This command is executed after a preset is applied.")
    box = self.get_content_area()
    box.pack_start(label, True, True, 0)
    self.entry = Gtk.Entry()
    self.entry.set_text(existing_post_command)
    box.pack_start(self.entry, True, True, 0)
    self.show_all()

  def get_text(self):
    return self.entry.get_text()


class Preset:
  def __init__(self, name, screens=[]):
    self.name = name
    self.screens = screens

  def command(self):
    res = 'xrandr'
    prev_monitor = ""
    for screen_index in range(len(available_screens)):
      res = res + ' --output ' + available_screens[screen_index]
      if self.screens[screen_index]:
        res = res + " --auto"
        if prev_monitor:
          res = res + " --right of " + prev_monitor
        prev_monitor = available_screens[screen_index]
      else:
        res = res + " --off"

    return res

def detect_screens():
  res = []
  randr = bytes.decode(subprocess.check_output("xrandr"))
  for line in randr.split('\n'):
    if ":" not in line:
      if len(line) > 0 and line[0:2] != "  ":
        res.append(line.split(" ")[0])
  return res


configfilename = os.environ["HOME"] + "/" + ".randrpresets.json"
with open(configfilename, 'r') as configfile:
  config = configfile.read()
  configdic = json.loads(config)
presets = configdic["presets"]
post_command = configdic["post_command"]
# available_screens = detect_screens() TODO detect screens when editing config
available_screens = configdic["screens"]
preset_list = []
for preset in presets:
  preset_list.append(Preset(preset[0], preset[1]))

win = RandrPresetsWindow(preset_list, post_command)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

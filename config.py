presets =\
  [
    ["Only internal", [["eDP1", True], ["VGA1", False], ["HDMI1", False]]],
    ["Internal+VGA", [["eDP1", True], ["VGA1", True], ["HDMI1", False]]],
    ["Internal+HDMI", [["eDP1", True], ["VGA1", False], ["HDMI1", True]]]
  ]

post_command = "sh ~/.i3/wmstuff.sh"

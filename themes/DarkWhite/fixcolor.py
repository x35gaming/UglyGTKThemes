#!/bin/python
import re
import sys
import os
import shutil

def hex_to_rgb(hex_code):
  """
  Converts a hex color code to RGB values.
  """
  if not hex_code.startswith('#') or len(hex_code) != 7:
    return None
  r, g, b = (int(hex_code[i:i+2], 16) for i in (1, 3, 5))
  return r, g, b

def rgb_to_luminance(r, g, b):
  """
  Calculates the luminance (average) of RGB values.
  """
  return int(0.299 * r + 0.587 * g + 0.114 * b)

def convert_color(color_string):
  """
  Converts a color string (hex, rgb, or rgba) to grayscale and replaces original value.
  """
  match = None
  if color_string.startswith('#'):
    r, g, b = hex_to_rgb(color_string)
    match = True
  elif 'rgb' in color_string:
    match = re.match(r'rgb?\((\d+),\s*(\d+),\s*(\d+)\)', color_string)
    if match:
      r, g, b = map(int, match.groups())
  elif 'rgba' in color_string:
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', color_string)
    if match:
      r, g, b, _ = map(int, match.groups())
  
  if match:
    luminance = rgb_to_luminance(r, g, b)
    new_color = "#" + (f"{luminance:02x}" * 3) if color_string.startswith('#') else f"rgb({luminance},{luminance},{luminance})"
    if 'rgba' in color_string:
      new_color += f", {match.group(4)}"
    return new_color
  return None

def process_css_file(filename):
  """
  Reads a CSS file, replaces color values with grayscale equivalents, and saves the changes.
  """
  # Create a backup filename
  backup_filename = os.path.join(os.path.dirname(filename), os.path.basename(filename) + ".old")

  # Copy the original file to the backup
  shutil.copy(filename, backup_filename)

  # Open the original file for reading
  with open(backup_filename, 'r') as f_in:
    # Create a new file for writing the modified content
    with open(filename, 'w') as f_out:
      for line in f_in:
        new_line = line
        for match in re.finditer(r'(#[0-9a-f]{6}|#[0-9A-F]{6}|rgb?\(\d+,\s*\d+,\s*\d+\)|rgba?\(\d+,\s*\d+,\s*\d+,\s*\d+\))', line):
          color_string = match.group()
          grayscale_color = convert_color(color_string)
          if grayscale_color:
            new_line = new_line.replace(color_string, grayscale_color)
        f_out.write(new_line)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    process_css_file(sys.argv[1])
  else:
    print('Please provide a CSS filename as an argument.')

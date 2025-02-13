import sys
import os
import imghdr
from collections import defaultdict
import cv2
import random
from PIL import Image, ImageDraw, ImageFont
import itertools
import threading
import time
import ntpath
import numpy as np

BRIGHTNESS = {'0': 0.9629629629629629,
              '1': 0.7407407407407407,
              '2': 0.8148148148148148,
              '3': 0.7777777777777778,
              '4': 0.8148148148148148,
              '5': 0.8888888888888888,
              '6': 0.8888888888888888,
              '7': 0.7037037037037037,
              '8': 0.9259259259259259,
              '9': 0.8888888888888888,
              'a': 0.7777777777777778,
              'b': 0.8888888888888888,
              'c': 0.5925925925925926,
              'd': 0.9629629629629629,
              'e': 0.6666666666666666,
              'f': 0.7777777777777778,
              'g': 0.9629629629629629,
              'h': 0.8888888888888888,
              'i': 0.6666666666666666,
              'j': 0.7037037037037037,
              'k': 0.8888888888888888,
              'l': 0.7407407407407407,
              'm': 0.6666666666666666,
              'n': 0.7037037037037037,
              'o': 0.6666666666666666,
              'p': 0.9259259259259259,
              'q': 0.9629629629629629,
              'r': 0.6296296296296297,
              's': 0.7037037037037037,
              't': 0.7407407407407407,
              'u': 0.7777777777777778,
              'v': 0.5555555555555556,
              'w': 0.6666666666666666,
              'x': 0.7407407407407407,
              'y': 0.8148148148148148,
              'z': 0.7037037037037037,
              'A': 0.8518518518518519,
              'B': 0.8888888888888888,
              'C': 0.7037037037037037,
              'D': 0.8888888888888888,
              'E': 0.8148148148148148,
              'F': 0.6666666666666666,
              'G': 0.8148148148148148,
              'H': 1.0,
              'I': 0.5925925925925926,
              'J': 0.6296296296296297,
              'K': 0.8518518518518519,
              'L': 0.6666666666666666,
              'M': 0.7777777777777778,
              'N': 0.8888888888888888,
              'O': 0.8148148148148148,
              'P': 0.7777777777777778,
              'Q': 0.8888888888888888,
              'R': 0.9259259259259259,
              'S': 0.7777777777777778,
              'T': 0.6666666666666666,
              'U': 0.8888888888888888,
              'V': 0.6666666666666666,
              'W': 0.7407407407407407,
              'X': 0.7407407407407407,
              'Y': 0.7407407407407407,
              'Z': 0.8148148148148148,
              '!': 0.37037037037037035,
              '"': 0.2222222222222222,
              '#': 0.8148148148148148,
              '$': 1.0,
              '%': 0.7777777777777778,
              '&': 0.7407407407407407,
              "'": 0.14814814814814814,
              '(': 0.4444444444444444,
              ')': 0.4444444444444444,
              '*': 0.3333333333333333,
              '+': 0.3333333333333333,
              ',': 0.14814814814814814,
              '-': 0.18518518518518517,
              '.': 0.07407407407407407,
              '/': 0.2962962962962963,
              '\\': 0.2962962962962963,
              ':': 0.14814814814814814,
              ';': 0.2222222222222222,
              '<': 0.37037037037037035,
              '=': 0.2962962962962963,
              '>': 0.37037037037037035,
              '?': 0.4444444444444444,
              '@': 0.8888888888888888,
              '[': 0.6666666666666666,
              ']': 0.6666666666666666,
              '^': 0.2962962962962963,
              '_': 0.2222222222222222,
              '`': 0.14814814814814814,
              '{': 0.5925925925925926,
              '|': 0.25925925925925924,
              '}': 0.5925925925925926,
              '~': 0.2222222222222222}

SPIN = True

# check if the args are valid
def check_args():
  # check if there are the right number of args
  if len(sys.argv) != 4:
    print('Expected 2 argument, got ' + str(len(sys.argv) - 1))
    sys.exit(1)

  # check if the first arg is a valid file
  if not is_valid_file(sys.argv[1]):
    sys.exit(1)

  # check if the second arg is a string
  if not isinstance(sys.argv[2], str):
    print('Expected a string, got ' + str(sys.argv[2]))
    sys.exit(1)

  # check if the third arg is a string
  if not isinstance(sys.argv[3], str):
    print('Expected a string, got ' + str(sys.argv[3]))
    sys.exit(1)

  # check if the third arg is a valid resolution scaling
  if int(sys.argv[3]) < 0 or int(sys.argv[3]) > 100:
    print('Expected a resolution scaling between 0 and 100, got ' + sys.argv[3])
    sys.exit(1)

# checks if the file is a valid image
def is_valid_file(file_path):
  if not isinstance(file_path, str):
    print('Expected a string, got ' + str(type(file_path)))
    return False
  if not os.path.isfile(file_path):
    print('File does not exist: ' + file_path)
    return False
  if not imghdr.what(file_path):
    print('File is not an image: ' + file_path)
    return False
  return True

def fetch_characters():
  # get the characters from the command line
  characters = sys.argv[2]

  ret = defaultdict(list)

  for character in characters:
    key = BRIGHTNESS[character]
    if character not in ret[key]:
      ret[key].append(character)

  return ret

def generate_ascii_art(image, resolution, characters):
  image = cv2.imread(image)
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  resized_gray_image = cv2.resize(gray_image, (int(image.shape[1] * resolution/100), int(image.shape[0] * resolution/100)))
  kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
  sharpened_image = cv2.filter2D(resized_gray_image, -1, kernel)
  resized_gray_image = sharpened_image

  height = resized_gray_image.shape[0]
  width = resized_gray_image.shape[1]

  brightness_map = get_mapping(characters)

  ascii_art = ''

  for y in range(height//2):
    for x in range(width):
      brightness_top = int(resized_gray_image[y*2, x])
      brightness_bottom = int(resized_gray_image[(y*2)+1, x])
      brightness = int((brightness_top + brightness_bottom)/2)
      ascii_art += random.choice(brightness_map[brightness])
    ascii_art += '\n'

  return ascii_art

def get_mapping(characters):

  map = defaultdict(str)
  map[0] = [' ']

  for i in range(1, 256):
    brightness = i/255
    keys = sorted(list(characters.keys()))
    l = 0
    r = len(keys) - 1
    old_m = None
    while l < r:
      m = int((l + r)//2)
      if old_m == m:
        break
      if brightness < keys[m]:
        r = m - 1
      elif brightness > keys[m]:
        l = m + 1
      elif brightness == keys[m]:
        break
      old_m = m
    map[i] = characters[keys[m]]

  return map

def save_ascii_art(art, path, resolution):
  basename = ntpath.basename(path)
  filename = ntpath.splitext(basename)[0]

  # save the ascii art to a text file
  with open('generated_text/' + filename + str(resolution) + '.txt', 'w') as f:
    f.write(art)

  lines = art.splitlines()
  image_width = max(len(line) for line in lines) * 7
  image_height = len(lines) * 12

  image = Image.new('RGB', (image_width, image_height), color=(0, 0, 0))
  d = ImageDraw.Draw(image)
  font = ImageFont.truetype('fonts/CascadiaCode.ttf', size=12)

  y_pos = 0
  for line in lines:
    d.text((0, y_pos), line, font=font, fill=(255, 255, 255))
    y_pos += 12

  image.save('generated_images/' + filename + '-' + str(resolution) + '.jpg', quality=10, optimize=True)

class SpinnerThread(threading.Thread):
    def __init__(self, message, delay=0.1):
        super().__init__(daemon=True)
        self.message = message
        self.delay = delay
        self._stop_event = threading.Event()

    def run(self):
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        while not self._stop_event.is_set():
            print(f"\r{self.message} {next(spinner)}", end="")
            time.sleep(self.delay)
        print("\r" + " " * (len(self.message) + 2) + "\r", end="")

    def stop(self):
        self._stop_event.set()
        self.join()

def main():
  check_args()
  characters = fetch_characters()
  art = generate_ascii_art(sys.argv[1], int(sys.argv[3]), characters)
  save_ascii_art(art, sys.argv[1], sys.argv[3])

if __name__ == '__main__':
  spinner = SpinnerThread("Generating ascii art...")
  spinner.start()

  main()

  spinner.stop()

  print("Saved ascii art as .txt to generated_text/ and as jpg to generated_images/")
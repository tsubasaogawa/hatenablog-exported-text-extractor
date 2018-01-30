# coding: utf-8

import os
import re
import sys
import codecs
import tempfile


class Config:
  # regex patterns
  regex = {
    'separator': r'^-----',
    'body': r'^BODY:',
    'html': r'<[^>]+>',
    'uri': r'https?://[a-zA-Z0-9!#$%&-~+,.?/_]+',
    'blank_line': r'$^'  # no match
  }

  # Remove it from text if True
  remove_flags = {
    'html': True,
    'uri': True,
    'blank_line': True
  }

  # compile regexes
  patterns = {}
  for key in regex.keys():
    patterns[key] = re.compile(regex[key])

  @staticmethod
  def get_remove_flags():
    return Config.remove_flags

  @staticmethod
  def get_patterns():
    return Config.patterns


class HBETExtractor:
  def __init__(self, file):
    self.file = file

  def extract(self):
    body_flags = {'separator': False, 'body': False}
    return_items = []
    item = []
    patterns = Config.get_patterns()

    with open(self.file) as f:
      for line in f:
        # check if last line included 'BODY:'
        if body_flags['separator'] is True and body_flags['body'] is True:
          # BODY section ends
          if patterns['separator'].match(line):
            body_flags['separator'] = body_flags['body'] = False
            return_item = self._remove_waste_chars(''.join(item))
            return_items.append(return_item)
            item = []
            continue
          # BODY section continues
          else:
            item.append(line)

        # Header section check
        elif body_flags['separator'] is False and body_flags['body'] is False:
          # start separator?
          if patterns['separator'].match(line):
            body_flags['separator'] = True
            continue

        # last line was separator?
        elif body_flags['separator'] is True:
          # This line includes 'BODY'?
          if patterns['body'].match(line):
            body_flags['body'] = True
          else:
            body_flags['separator'] = False

    return return_items

  def _remove_waste_chars(self, line):
    remove_flags = Config.get_remove_flags()
    for pattern in remove_flags.keys():
      if remove_flags[pattern]:
        line = Config.get_patterns()[pattern].sub('', line)

    return line


def usage_and_exit():
  sys.stderr.write("usage: %s [input file] > [output file]\n" % sys.argv[0])
  sys.exit(1)

if __name__ == '__main__':
  temp_file = input_file = None

  # args check
  if len(sys.argv) == 1:
    stdin = sys.stdin.read()
    if stdin.rstrip() != '':
      with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_file = temp.name
        input_file = temp_file
        temp.write(stdin.encode())
    else:
      usage_and_exit()
  else:
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
      usage_and_exit()

  # instance
  extractor = HBETExtractor(input_file)

  # extract
  extracted_text = ''.join(extractor.extract())
  print(extracted_text, "\n")

  if temp_file is not None:
    os.remove(temp_file)

  sys.exit(0)

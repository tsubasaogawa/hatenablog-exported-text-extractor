# coding: utf-8

import os
import re
import sys, codecs

# regex patterns
regex = {
  'separator': r'^-----',
  'body': r'^BODY:',
  'html': r'<[^>]+>',
  'uri': r'https?://[a-zA-Z0-9!#$%&-~+,.?/_]+',
  'blank_line': r'$^' # no match
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

class HBETExtractor:
  def __init__(self, file):
    self.file = file

  def extract(self):
    body_flags = {'separator': False, 'body': False}
    return_items = []
    item = []
    with open(self.file) as f:
      for line in f:
        # 以前の行が BODY: だった
        if body_flags['separator'] == True and body_flags['body'] == True:
          # BODY: フィールド終了
          if pattern['separator'].match(line):
          if patterns['separator'].match(line):
            body_flags['separator'] = False
            body_flags['body'] = False
            return_item = self.__remove_waste_chars(''.join(item))
            return_items.append(return_item)
            item = []
            continue
          else:
            item.append(line)

        # ヘッダ部
        elif body_flags['separator'] == False and body_flags['body'] == False:
          # ---- を探す
          if patterns['separator'].match(line):
            body_flags['separator'] = True
            continue

        # 前行が ----- だった
        elif body_flags['separator'] == True:
          # BODY: であるかどうか
          if patterns['body'].match(line):
            body_flags['body'] = True
          else:
            body_flags['separator'] = False

    return return_items

  def __remove_waste_chars(self, line):
    for pattern in remove_flags.keys():
      if remove_flags[pattern]:
        line = patterns[pattern].sub('', line)

    return line

if __name__ == '__main__':
  input_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/test.txt'
  if not os.path.exists(input_file):
    sys.stderr.write('No file exists: ', input_file)
    sys.exit(1)

  extractor = HBETExtractor(input_file)
  et = extractor.extract()
  print(''.join(et))

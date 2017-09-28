# coding: utf-8

import re
import sys, codecs

# sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

regex = {
  'separator': r'^-----',
  'body': r'^BODY:',
  'html': r'<[^>]+>',
  'uri': r'https?://'
}
pattern = {}
for key in regex.keys():
  pattern[key] = re.compile(regex[key])

REMOVE_TAG = True

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
          if pattern['separator'].match(line):
            body_flags['separator'] = True
            continue

        # 前行が ----- だった
        elif body_flags['separator'] == True:
          # BODY: であるかどうか
          if pattern['body'].match(line):
            body_flags['body'] = True
          else:
            body_flags['separator'] = False

    return return_items

  def __remove_waste_chars(self, line):
    line_no_uri = pattern['uri'].sub('', line)
    line_no_uri_html = pattern['html'].sub('', line_no_uri)
    return line_no_uri_html

if __name__ == '__main__':
  extractor = HBETExtractor('/tmp/test.txt')
  print(''.join(extractor.extract()).encode('utf-8'))

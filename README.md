# hatenablog-exported-text-extractor

## Overview

* Extract only text from an exported text file from hatenablog (www.hatenablog.com)
* Optional: the following elements are ignored
  * Metadata (AUTHOR, TITLE, ...)
  * HTML tags
  * URI

## Example

### Before

```
AUTHOR: tsubasaogawa
TITLE: お天気Meteo
BASENAME: 2016/03/14/162112
STATUS: Publish
ALLOW COMMENTS: 1
CONVERT BREAKS: 0
DATE: 03/14/2016 16:21:12
CATEGORY: music
-----
 BODY:
 <p><iframe src="//www.youtube.com/embed/7dwCGG9bbn4" width="420" height="315" frameborder="0" allowfullscreen=""></iframe><br />      <a href="https://youtube.com/watch?v=7dwCGG9bbn4">お天気Ｍｅｔｅｏ／BSN新潟放送</a></p>
 <p>我が地元新潟のお話。</p>
 <p><a class="keyword" href="http://d.hatena.ne.jp/keyword/%BF%B7%B3%E3%CA%FC%C1%F7">新潟放送</a>では「お天気Meteo」という夜の天>      気予報番組があって、これがまたカッコイイ。</p>
<p>こういう動画を自宅にプロジェクターで投影しながら何となく悦に浸りたい。</p>
 ```

### After

```
お天気Ｍｅｔｅｏ／BSN新潟放送
我が地元新潟のお話。
新潟放送では「お天気Meteo」という夜の天気予報番組があって、これがまたカッコイイ。
こういう動画を自宅にプロジェクターで投影しながら何となく悦に浸りたい。
```

## Usage

```bash
# use args
$ python ./extractor.py [input file] > [output file]

# or stdin
$ cat [input file] | python ./extractor.py > [output file]
```

## Requirements

* Python 3

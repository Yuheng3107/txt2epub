import re
import os
import html
import chardet
import codecs
import zhconv

CHAPTER_RE = re.compile(r'第([\d一二三四五六七八九十百千]+)章')
NUM_CHAPTER_RE = re.compile(r'^\s*([1-9]\d*)\s*[：:]\s*\S')


def _chapter_match(line):
    m = CHAPTER_RE.search(line)
    if m:
        return _cn_to_int(m.group(1)), m.start()
    m = NUM_CHAPTER_RE.match(line)
    if m:
        return int(m.group(1)), m.start()
    return None, -1


def _chapter_title(line):
    m = CHAPTER_RE.search(line)
    if m:
        return line[m.end():].strip()
    m = NUM_CHAPTER_RE.match(line)
    if m:
        return line[m.end():].strip()
    return None

# ponytail: Chinese numeral → int
_CN_DIGITS = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
_CN_UNITS = {'十':10, '百':100, '千':1000}

def _cn_to_int(s):
    if s.isdigit():
        return int(s)
    n = 0
    section = 0
    for ch in s:
        if ch in _CN_DIGITS:
            section = _CN_DIGITS[ch]
        elif ch in _CN_UNITS:
            unit = _CN_UNITS[ch]
            section = (section or 1) * unit
            if unit >= 10:
                n += section
                section = 0
    return n + section


def convert_traditional(book_name):
    with open(book_name, "r") as f:
        data = f.read()
    if zhconv.convert(data, "zh-cn") != data:
        print("Converting Traditional to Simplified Chinese")
        data = zhconv.convert(data, "zh-cn")
        with open(book_name, "w") as newfile:
            newfile.write(data)


def correct_encoding(book_name):
    with codecs.open(book_name, "r", "gb18030") as f:
        print("Converting Encoding")
        data = f.read()
        # ponytail: unescape nested HTML entities like &amp;amp;#34;
        while True:
            unescaped = html.unescape(data)
            if unescaped == data:
                break
            data = unescaped
        data = data.replace("<", "&lt;")
        data = data.replace(">", "&gt;")
        with codecs.open(book_name, "w", "utf-8") as newfile:
            newfile.write(data)


def check_encoding(book_name):
    with open(book_name, "rb") as f:
        data = f.read(10000)
        encoding = chardet.detect(data)['encoding']
        if encoding != 'utf-8':
            correct_encoding(book_name)
        else:
            clean_xml(book_name)
            print("XML Cleaned")
    
def clean_xml(book_name):
    with open(book_name, "r") as file:
        ### Cleaning out things which are forbidden in XML
        data = file.read()
        # ponytail: unescape nested HTML entities like &amp;amp;#34;
        while True:
            unescaped = html.unescape(data)
            if unescaped == data:
                break
            data = unescaped
        data = data.replace("<", "&lt;")
        data = data.replace(">", "&gt;")
        with open(book_name, "w") as newfile:
            newfile.write(data)
             
            








def parse(book_name):
    check_encoding(book_name)
    convert_traditional(book_name)
    title = zhconv.convert(book_name, "zh-cn")
    with open(book_name) as f:
        chapter_names = list()
        chapter_contents = list()
        counter = -1
        expected_chapter = 1
        last_title = None
        for line in f:
            if line == "\n":
                continue
            chapter_num, start = _chapter_match(line)
            # ponytail: skip stale duplicate markers (same title as the chapter just opened)
            if chapter_num is not None and _chapter_title(line) == last_title:
                chapter_num = None
            # ponytail: accept any chapter >= expected to survive gaps/dupes
            if chapter_num is not None and chapter_num >= expected_chapter:
                if counter == -1:
                    # first chapter: strip "N." prefix if present
                    stripped = line.strip()
                    pm = re.match(r'\d+\.', stripped)
                    if pm:
                        stripped = stripped[pm.end():]
                        line = stripped + '\n'
                    if not (stripped.startswith('第') or NUM_CHAPTER_RE.match(stripped)):
                        continue
                else:
                    if start > 0:
                        # inline chapter: split text before marker into current chapter
                        chapter_contents[counter].append(line[:start])
                        line = line[start:]
                # standalone or inline: start new chapter
                chapter_names.append(line)
                counter += 1
                chapter_contents.append([])
                expected_chapter = chapter_num + 1
                last_title = _chapter_title(line)
            if counter > -1:
                chapter_contents[counter].append(line)
        return (title, chapter_names, chapter_contents)

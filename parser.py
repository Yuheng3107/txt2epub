import re
import os
import chardet
import codecs
def correct_encoding(book_name):
    with codecs.open(book_name, "r", "gb18030") as f:
        data = f.read()
        data = data.replace("&", "&amp;")
        data = data.replace("<", "&lt;")
        data = data.replace(">", "&gt;")
        with codecs.open(book_name, "w", "utf-8") as newfile:
            newfile.write(data)


def check_encoding(book_name):
    with open(book_name, "rb") as f:
        print('test')
        return
        data = f.read(100)
        print(data)
        encoding = chardet.detect(data)['encoding']
        print(encoding)
        if encoding != 'utf-8':
            correct_encoding(book_name)
            return
    with open(book_name, "r") as file:
        ### Cleaning out things which are forbidden in XML
        data = file.read()
        data = data.replace("&", "&amp;")
        data = data.replace("<", "&lt;")
        data = data.replace(">", "&gt;")
        with open(book_name, "w") as newfile:
            newfile.write(data) 
             
            








def parse(book_name):
    check_encoding(book_name)
    with open(book_name) as f:
        chapter_names = list()
        chapter_contents = list()
        counter = -1
        for line in f:
            if line == "\n":
                continue
            if line.strip().startswith("第") and line.find("章") != -1:
                chapter_names.append(line)
                counter += 1
                empty_list = list()
                chapter_contents.append(empty_list)
            if counter > -1:
                chapter_contents[counter].append(line)
        return (book_name, chapter_names, chapter_contents)

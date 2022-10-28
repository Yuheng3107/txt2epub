# txt2epub
#### Video Demo: https://youtu.be/yDBaujjy0DQ
#### Description
A simple project that converts a txt to epub file. Currently, this is purposed for parsing a chinese novel and converting it into .epub format for easy reading, but it can be tweaked for other purposes (Mostly novels).

Dependencies: chardet and codec

How it works:
The code in main.py detects the encoding and changes it to utf-8 if it is in the gb family of encodings (Chinese encoding). Subsequently, it parses the file to produce the components required for an epub file and zips them all together to form the epub file, removing the files created in the process.

Usage: 
To convert a chinese novel (.txt) file into epub format for reading on Apple Books, simply run the main.py code (python3 main.py) and when the prompt shows up, input the name of the novel, and a .epub file will be produced.

I started on this project because it was becoming increasingly difficult to find .epub formats of chinese novels online, and downloading the txt files and converting them through txt to epub websites was not only slow, but had various limitations as there were restrictions on the size and number of files I could upload. Moreover, the format was not customizable, and there were often issues that I could not fix. I then tried to use other pre-built applications to produce .epub files, but they too were ridiculously slow (taking hours at times) and not producing the results I wanted. I even tried cloning projects on github, but the documentation was esoteric, and some of them were outdated (python 2), and not producing the results I wanted.
As such, I decided to take things into my own hands, and after a few days of work, I made this prototype that only takes a few seconds to produce an epub file from a txt file. Makes one wonder why the websites take hours to do so...

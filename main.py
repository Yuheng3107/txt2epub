# This project to convert a txt file (chinese novel) into epub format for easy reading
import os
import re
import subprocess
from parser import parse


# Add path to OEBPS here
OEBPS_PATH = "zipping area/OEBPS"
# Changes the title in the cover.html file
def edit_cover(title):
    filepath = os.path.join(OEBPS_PATH, "cover.html")
    with open(filepath, "w") as f:
        index = title.find(".")
        title = title[:index]
        data = """<?xml version="1.0" encoding="utf-8" ?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
        <head>
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <meta name="generator" content="EasyPub v1.50" />
        <title>
        Cover
        </title>
        <style type="text/css">
        html,body {height:100%; margin:0; padding:0;}
        .wedge {float:left; height:50%; margin-bottom: -360px;}
        .container {clear:both; height:0em; position: relative;}
        table, tr, th {height: 720px; width:100%; text-align:center;}
        </style>
        <link rel="stylesheet" href="style.css" type="text/css"/>
        </head>
        <body>
        <div class="wedge"></div>
        <div class="container">
        <table><tr><td>"""
        additional_data =  f"""\n<img src="cover.jpg" alt='{title}'/>
        </td></tr></table>
        </div>
        </body>
        </html> """
        data = data + additional_data
        with open(filepath, "w") as newfile:
            newfile.write(data)
### Checked, is working


def edit_toc_ncx(title, chapter_names):
    filepath = os.path.join(OEBPS_PATH, "toc.ncx")
    with open(filepath, "w") as newfile:
        data = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="cover" content="cover"/>
<meta name="dtb:uid" content="easypub-12fb1042" />
<meta name="dtb:depth" content="1"/>
<meta name="dtb:generator" content="EasyPub v1.50"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>"""
        data = data + f"""<docTitle><text>{title}</text></docTitle> <docAuthor>
        <text></text>
        </docAuthor>"""
        navlist = list()
        for num, chapter_name in enumerate(chapter_names):
            navPoint = f"""<navPoint id="chapter{num}" playOrder='{num+3}'><navLabel><text>{chapter_name}</text></navLabel>
                <content src="chapter{num}.html"/>
                </navPoint>"""
            navlist.append(navPoint)
        navMap = """<navMap>
            <navPoint id="cover" playOrder="1">
            <navLabel><text>封面</text></navLabel>
            <content src="cover.html"/>
            </navPoint>
            <navPoint id="htmltoc" playOrder="2">
            <navLabel><text>目录</text></navLabel>
            <content src="book-toc.html"/>
            </navPoint>"""
        navMap = navMap + ' '.join(navlist) + "</navMap>"
        ### navMap is working
        data = data + navMap + "</ncx>"
        newfile.write(data)

### Edits the book-toc.html file and changes the numbers and chapter_names
def edit_book_toc_html(chapter_names):
    filepath = os.path.join(OEBPS_PATH, "book-toc.html")
    with open(filepath, "w") as newfile:
        data = """<?xml version="1.0" encoding="utf-8" ?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
        <head>
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <meta name="generator" content="EasyPub v1.50" />
        <title>
        Table Of Contents
        </title>
        <link rel="stylesheet" href="style.css" type="text/css"/>
        </head>
        <body>
        <h2 class="titletoc">
        目录
        </h2>
        <div class="toc">"""
        datalist = list()
        for num, chapter_name in enumerate(chapter_names):
            datalist.append(f"""<dt class="tocl2"><a href="chapter{num}.html">{chapter_name}</a></dt>""")
        joined_datalist = "\n".join(datalist)
        dl = f'<dl> {joined_datalist} </dl>'
        data = data + dl + "\n</div>\n</body>\n</html>\n"
        newfile.write(data)


def edit_content_opf(title, chapter_names):
    filepath = os.path.join(OEBPS_PATH, "content.opf")
    with open(filepath, "w") as newfile:
        data = f"""<?xml version="1.0" encoding="utf-8" standalone="no"?>

<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:identifier id="bookid">easypub-12fb1042</dc:identifier>
<dc:title>{title}</dc:title>
<dc:date>2019</dc:date>
<dc:rights>Created with EasyPub v1.50</dc:rights>
<dc:language>zh-CN</dc:language>
<meta name="cover" content="cover-image"/>
</metadata>
<manifest>
<item id="ncxtoc" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
<item id="htmltoc"  href="book-toc.html" media-type="application/xhtml+xml"/>
<item id="css" href="style.css" media-type="text/css"/>
<item id="cover-image" href="cover.jpg" media-type="image/jpeg"/>
<item id="cover" href="cover.html" media-type="application/xhtml+xml"/> """
        itemlist = list()
        for num, chapter_name in enumerate(chapter_names):
            item = f"""<item id="chapter{num}" href="chapter{num}.html" media-type="application/xhtml+xml"/>"""
            itemlist.append(item)
        data = data + "\n".join(itemlist) + "\n</manifest>\n"
        spine = """<spine toc="ncxtoc">
            <itemref idref="cover" linear="no"/>
            <itemref idref="htmltoc" linear="yes"/>
            """
        itemlist = list()
        for num, chapter in enumerate(chapter_names):
            item = f'<itemref idref="chapter{num}" linear="yes"/>'
            itemlist.append(item)
        spine = spine + "\n".join(itemlist) + "\n</spine>\n"
        data = data + spine
        additional_data = """<guide>
        <reference href="cover.html" type="cover" title="Cover"/>
        <reference href="book-toc.html" type="toc" title="Table Of Contents"/>
        <reference href="chapter0.html" type="text" title="Beginning"/>
        </guide>
        </package>"""
        data = data + additional_data
        newfile.write(data)
### Creates the chapter{num}.html files
def create_chapters(chapter_names, chapter_contents):
    for num, chapter_name in enumerate(chapter_names):
        filepath = os.path.join(OEBPS_PATH, f"chapter{num}.html")
        with open(filepath, "w") as f:
            data = f"""<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
<meta name="generator" content="EasyPub v1.50" />
<title>{chapter_name}</title>
<link rel="stylesheet" href="style.css" type="text/css"/>
</head>
<body>
<h2 id="title" class="titlel2std">{chapter_name}</h2>"""
            contents = list()
            for line in chapter_contents[num]:
                line = f'<p class="a">{line}</p><br/>'
                contents.append(line)
            data = data + "\n".join(contents) + "</body> \n </html>"
            f.write(data)
def create_epub(title):
    ## zip -0Xq book.epub mimetype (Adds mimetype as first file, uncompressed)
    zipping_area = os.path.join(os.getcwd(), "zipping area")
    book_name = f"{title}.epub"
    subprocess.run(["zip", "-0Xq", book_name, "mimetype"], cwd=zipping_area)
    subprocess.run(f"zip -Xr9Dq {book_name} * -x mimetype -x {book_name}", cwd=zipping_area, shell=True)
    subprocess.run(["mv", book_name, "../"], cwd= zipping_area)
    ## zip -Xr9Dq book.epub * -x mimetype -x book.epub
    subprocess.run(["rm *.html"], cwd=OEBPS_PATH, shell=True)

def main():
    # Gives the title of the book. a list of the chapter names, as well as a list of chapter contents
    # -each chapter content will be a list of lines
    book_name = input("Enter the name of the book: ")
    if book_name.find(".txt") != -1:
        index = book_name.find(".txt")
        book_name = book_name[:index]
        subprocess.run(["mv", f"{book_name}.txt", book_name])
    title, chapter_names, chapter_contents = parse(book_name)
    chapter_names = [chapter_name.strip() for chapter_name in chapter_names]
    edit_cover(title)
    edit_toc_ncx(title, chapter_names)
    edit_book_toc_html(chapter_names)
    edit_content_opf(title, chapter_names)
    create_chapters(chapter_names, chapter_contents)
    create_epub(title)

if __name__ == '__main__':
    main()

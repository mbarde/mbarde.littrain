# -*- coding: utf-8 -*-
from lxml import etree

import logging
import zipfile


class EPubReader:

    def __init__(self, file):
        self.file = file
        self.zipFile = zipfile.ZipFile(self.file.open())

    def getChapters(self):
        contents = self.zipFile.namelist()

        tocFileName = False
        for filename in contents:
            if filename[-4:] == '.ncx':
                tocFileName = filename
                break

        if tocFileName is False:
            logging.error('[ePub reader] No TOC found')
            return []

        tocFile = self.zipFile.open(tocFileName)
        tocContent = tocFile.read()
        tocXML = etree.fromstring(tocContent)

        chaptersXML = tocXML.xpath(
            '//x:navPoint[@class="chapter"]',
            namespaces={'x': 'http://www.daisy.org/z3986/2005/ncx/'})

        chapters = []

        for chapterXML in chaptersXML:
            titleXML = chapterXML.find('{http://www.daisy.org/z3986/2005/ncx/}navLabel')
            title = titleXML.find('{http://www.daisy.org/z3986/2005/ncx/}text').text
            contentXML = chapterXML.find('{http://www.daisy.org/z3986/2005/ncx/}content')
            src = contentXML.get('src')

            chapterFile = self.zipFile.open(src)
            content = chapterFile.read()

            parser = etree.HTMLParser(encoding='utf-8')
            contentHTML = etree.fromstring(content, parser=parser)
            content = ''.join(contentHTML.itertext()).decode('utf-8')

            chapters.append({
                'title': title,
                'content': content,
            })

        return chapters

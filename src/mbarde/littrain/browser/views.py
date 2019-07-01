# -*- coding: utf-8 -*-
from mbarde.littrain.epub import EPubReader
from mbarde.littrain.lemma import LemmaCollector
from mbarde.littrain.lemma import LemmaStorer
from Products.Five.browser import BrowserView

import sys


reload(sys)
sys.setdefaultencoding('utf8')


class ReadEPubView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getChapters(self):
        if self.context.portal_type != 'File':
            return []
        self.ePubReader = EPubReader(self.context.file)
        return self.ePubReader.getChapters()

    def getLemmas(self):
        if self.context.portal_type != 'File':
            return []

        lemmaCollector = LemmaCollector()
        ePubReader = EPubReader(self.context.file)

        c = 0
        for chapter in ePubReader.getChapters():
            lemmaCollector.updateLemmasByChapter(chapter['content'], chapter['title'])
            c += 1
            if c > 0:
                break

        storer = LemmaStorer(self.context.title)
        lemmaCollector.storeLemmas(storer)

# -*- coding: utf-8 -*-
from mbarde.littrain.epub import EPubReader
from mbarde.littrain.lemma import LemmaCollector
from mbarde.littrain.lemma import LemmaStorer
from Products.Five.browser import BrowserView

import logging
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class ReadEPubView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.difficulty = 4  # the higher the easier

    def getChapters(self):
        if self.context.portal_type != 'File':
            return []
        self.ePubReader = EPubReader(self.context.file)
        return self.ePubReader.getChapters()

    def getLemmas(self):
        if self.context.portal_type != 'File':
            return []

        logging.info('Initializing and reading EPUB file ({0})'.format(
            str(self.context)))
        lemmaCollector = LemmaCollector()
        ePubReader = EPubReader(self.context.file)

        c = 0
        for chapter in ePubReader.getChapters():
            if c > 7:
                logging.info('Updating lemmas by chapter {0} ({1}) ...'.format(
                    chapter['title'], str(c)))
                lemmaCollector.updateLemmasByChapter(chapter['content'], chapter['title'])
            c += 1

        storer = LemmaStorer(self.context.title)
        logging.info('Storing {0} lemmas ...'.format(str(lemmaCollector.getLemmasCount())))
        lemmaCollector.storeLemmas(storer, maxOccurence=self.difficulty)

        logging.info('Done storing {0} lemmas.'.format(str(lemmaCollector.getLemmasCount())))

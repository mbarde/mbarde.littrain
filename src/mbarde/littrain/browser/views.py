# -*- coding: utf-8 -*-
from mbarde.littrain.epub import EPubReader
from mbarde.littrain.lemma import LemmaCollector
from mbarde.littrain.lemma import LemmaStorer
from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser import BrowserView

import logging


class ReadEPubView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.difficulty = 1  # the higher the easier

    def getChapters(self):
        if self.context.portal_type != 'File':
            return []
        self.ePubReader = EPubReader(self.context.file)
        return self.ePubReader.getChapters()

    def __call__(self):
        chaptersToRead = self.request.form.get('chapter', False)
        if chaptersToRead is not False:
            if not isinstance(chaptersToRead, list):
                chaptersToRead = [chaptersToRead]
            updateDefinitions = self.request.form.get('updateDefinitions', False)
            self.readAndStoreLemmasFromChapters(chaptersToRead, updateDefinitions)
        return super(ReadEPubView, self).__call__()

    def readAndStoreLemmasFromChapters(self, chaptersToRead, updateDefinitions=True):
        if self.context.portal_type != 'File':
            return []

        logging.info('Initializing and reading EPUB file ({0})'.format(
            str(self.context)))
        lemmaCollector = LemmaCollector()
        ePubReader = EPubReader(self.context.file)

        c = 0
        for chapter in ePubReader.getChapters():
            if chapter['id'] in chaptersToRead:
                logging.info('Updating lemmas by chapter {0} ({1}) ...'.format(
                    chapter['title'], str(c)))
                lemmaCollector.updateLemmasByChapter(chapter['content'], chapter['title'])
            c += 1

        storer = LemmaStorer(self.context.title)
        logging.info('Storing {0} lemmas ...'.format(str(lemmaCollector.getLemmasCount())))
        lemmaCollector.storeLemmas(
            storer, maxOccurence=self.difficulty, updateDefinitions=updateDefinitions)

        logging.info('Done storing {0} lemmas.'.format(str(lemmaCollector.getLemmasCount())))


class LemmaView(DefaultView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        updateDefs = self.request.form.get('update-definitions', False)
        if updateDefs and self.canUpdateFromView():
            self.context.updateDefinitions()
        return super(LemmaView, self).__call__()

    def canUpdateFromView(self):
        return api.user.get_permissions(obj=self.context) \
            .get('Manage portal', False)

    def getModifiedLocalized(self):
        return api.portal.get_localized_time(self.context.modified(), long_format=True)

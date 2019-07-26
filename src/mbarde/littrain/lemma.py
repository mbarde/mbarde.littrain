# -*- coding: utf-8 -*-
from plone import api
from z3c.relationfield import RelationValue
from zope import component
from zope.intid.interfaces import IIntIds

import logging
import spacy


class LemmaContainer:
    """ Stores lemma and how often it occured in a book
        (and in which chapters) """

    def __init__(self, lemma, count=1, inChapters=[], partOfSpeech=''):
        self.lemma = lemma
        self.count = count
        self.inChapters = inChapters
        self.partOfSpeech = partOfSpeech

    def alsoOccuredInChapter(self, chapterTitle):
        self.count += 1
        if chapterTitle not in self.inChapters:
            self.inChapters.append(chapterTitle)

    def prettyPrint(self):
        return '{0} [{1}] ({2}x)\n{3}'.format(
            self.lemma.encode('utf-8'),
            self.partOfSpeech,
            str(self.count),
            str(self.inChapters))


class LemmaCollector:
    """ Can be used to collect lemmas of a book """

    def __init__(self):
        self.naturalLanguageProcessor = spacy.load('en_core_web_sm')
        self.lemmas = {}

    def updateLemmasByChapter(self, chapterText, chapterTitle):
        tokens = self.naturalLanguageProcessor(chapterText)

        for token in tokens:
            if token.is_stop is False \
               and token.is_punct is False \
               and token.pos_ != 'NUM' \
               and token.is_alpha is True:
                lemma = token.lemma_
                if lemma in self.lemmas:
                    self.lemmas[lemma].alsoOccuredInChapter(chapterTitle)
                else:
                    self.lemmas[lemma] = LemmaContainer(
                        lemma, 1, [chapterTitle], token.pos_)

    def getLemmasWithMaxOccurence(self, maxOccurence=1):
        results = []
        for lemma in self.lemmas:
            if self.lemmas[lemma].count <= maxOccurence:
                results.append(self.lemmas[lemma])
        return results

    def storeLemmas(self, storer, maxOccurence=None, updateDefinitions=False):
        if maxOccurence is None:
            lemmas = list(self.lemmas.values())
        else:
            lemmas = self.getLemmasWithMaxOccurence(maxOccurence)

        c = 0
        maxC = len(lemmas)
        reportSteps = 20
        for lemma in lemmas:
            storer.storeLemma(lemma, updateDefinitions)
            c += 1
            if c % reportSteps == 0:  # noqa: S001
                logging.info('Stored {0}% of all lemmas.'.format(
                    str(int(float(c) / float(maxC) * 100))))

    def getLemmasCount(self):
        return len(self.lemmas)


class LemmaStorer:
    """ Class to store lemmas as persistent objects within following structure:
        [Folder]
            -> [Book A]
                -> [Chapter 1]
                    -> [Lemma A]
                    -> [Lemma B]
                    -> ...
                -> [Chapter 2]
                -> ...
            -> [Book B]
            -> ...
    """

    bookContainerId = 'books'
    bookContainer = None
    book = None
    chapters = {}

    def __init__(self, bookTitle):
        self.bookContainer = None
        self.book = None
        self.chapters = {}
        self.bookContainer = self.getBookContainer()
        self.book = self.getBook(bookTitle)

    def storeLemma(self, lemma, updateDefinitions=False):
        # convert list of chapter titles into list of
        # RelationValue's pointing to chapter objects
        intids = component.getUtility(IIntIds)
        inChaptersRVs = []
        for chapterTitle in lemma.inChapters:
            chapterObj = self.getChapter(chapterTitle)
            inChaptersRVs.append(
                RelationValue(intids.getId(chapterObj)),
            )

        for chapterTitle in lemma.inChapters:
            chapterObj = self.getChapter(chapterTitle)
            data = {
                'lemma': lemma.lemma,
                'count': lemma.count,
                'chapters': inChaptersRVs,
                'partOfSpeech': lemma.partOfSpeech,
            }
            obj = api.content.create(
                type='Lemma',
                title=lemma.lemma,
                container=chapterObj,
                **data  # noqa: C815
            )
            if updateDefinitions:
                obj.updateDefinitions()

    def getBookContainer(self):
        if self.bookContainer is not None:
            return self.bookContainer

        portal = api.portal.get()
        bookContainer = portal.get(self.bookContainerId, None)
        if bookContainer is None:
            bookContainer = api.content.create(
                type='Folder',
                title=self.bookContainerId,
                id=self.bookContainerId,
                container=portal,
            )
        return bookContainer

    def getBook(self, bookTitle):
        if self.book is not None:
            return self.book

        book = api.content.create(
            type='Book',
            title=bookTitle,
            container=self.bookContainer,
        )
        return book

    def getChapter(self, chapterTitle):
        if chapterTitle not in self.chapters:
            self.chapters[chapterTitle] = api.content.create(
                type='Chapter',
                title=chapterTitle,
                container=self.book,
            )
        return self.chapters.get(chapterTitle)

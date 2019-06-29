# -*- coding: utf-8 -*-
import spacy


class LemmaContainer:
    ''' Stores lemma and how often it occured in a book
        (and in which chapters) '''

    def __init__(self, lemma, count=1, inChapters=[]):
        self.lemma = lemma
        self.count = count
        self.inChapters = inChapters

    def alsoOccuredInChapter(self, chapterTitle):
        self.count += 1
        if chapterTitle not in self.inChapters:
            self.inChapters.append(chapterTitle)

    def prettyPrint(self):
        return '{0} ({1}x)\n{2}'.format(
            self.lemma.encode('utf-8'),
            str(self.count),
            str(self.inChapters))


class LemmaCollector:
    ''' Can be used to collect lemmas of a book '''

    def __init__(self):
        self.naturalLanguageProcessor = spacy.load('en_core_web_sm')
        self.lemmas = {}

    def updateLemmasByChapter(self, chapterText, chapterTitle):
        tokens = self.naturalLanguageProcessor(chapterText)

        for token in tokens:
            if token.is_stop is False \
             and token.is_punct is False \
             and token.pos_ != 'NUM':
                lemma = token.lemma_
                if lemma in self.lemmas:
                    self.lemmas[lemma].alsoOccuredInChapter(chapterTitle)
                else:
                    self.lemmas[lemma] = LemmaContainer(lemma, 1, [chapterTitle])

    def getLemmasWithMaxOccurence(self, maxOccurence=1):
        results = []
        for lemma in self.lemmas:
            if self.lemmas[lemma].count <= maxOccurence:
                results.append(self.lemmas[lemma])
        return results

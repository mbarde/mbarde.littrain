# -*- coding: utf-8 -*-
from wiktionaryparser import WiktionaryParser


def fetchWord(lemma):
    parser = WiktionaryParser()
    fetchedWord = parser.fetch(lemma, 'english')
    parser.session.close()
    return fetchedWord


def getDefinitions(lemma):
    fetchedWord = fetchWord(lemma)
    definitions = []

    # merge definition lists of all etymologies
    for etymology in fetchedWord:
        defs = etymology.get('definitions', [])
        definitions += defs

    return definitions


# https://spacy.io/api/annotation#pos-en
# to
# https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech
def getPartOfSpeechWiktionaryStyle(partOfSpeech):
    mappings = {
        'PROPN': 'noun',
        'ADJ': 'adjective',
        'NOUN': 'noun',
        'VERB': 'verb',
        'ADV': 'adverb',
        'INTJ': 'interjection',
    }
    return mappings.get(partOfSpeech, partOfSpeech)


def adverbToAdjcetive(lemmaAdverb):
    fetchedWord = fetchWord(lemmaAdverb)
    if len(fetchedWord) == 0:
        return False
    etym = fetchedWord[0].get('etymology', '')
    if len(etym) == 0:
        return False
    # in Wiktionary articles of adverbs usually you find
    # following part in the etymology paragraph:
    # adjective (lyDelimiter) -ly
    # i.e. strong +\u200e -ly
    lyDelimiter = '+\u200e'
    if lyDelimiter not in etym:
        return False
    splitted = etym.split('+\u200e')
    if len(splitted) != 2:
        return False
    splitted = splitted[0].strip().split(' ')
    if len(splitted) == 0:
        return False
    adjLemma = splitted[-1].strip()
    return adjLemma

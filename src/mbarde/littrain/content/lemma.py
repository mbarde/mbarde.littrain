# -*- coding: utf-8 -*-
from mbarde.littrain import _
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.supermodel import model
from wiktionaryparser import WiktionaryParser
from z3c.relationfield import RelationChoice
from z3c.relationfield import RelationList
from zope import schema
from zope.interface import implementer


class ILemma(model.Schema):

    lemma = schema.TextLine(
        title=_(u'Lemma'),
        required=True,
    )

    count = schema.Int(
        title=_(u'Count'),
        description=_(u'How often does this lemma occur in the whole book?'),
        default=0,
        required=True,
    )

    chapters = RelationList(
        title=_(u'Chapters'),
        description=_(u'List of chapters in which this lemma occurs'),
        default=[],
        value_type=RelationChoice(
            source=CatalogSource(portal_type=['Chapter']),
        ),
        required=True,
    )

    partOfSpeech = schema.Text(
        title=_(u'Part of speech tag'),
        required=True,
    )

    definitions = schema.List(
        title=_(u'Definitions'),
        default=[],
        required=False,
    )

    relatedWords = schema.List(
        title=_(u'Related words'),
        default=[],
        required=False,
    )

    examples = schema.List(
        title=_(u'Examples'),
        default=[],
        required=False,
    )


@implementer(ILemma)
class Lemma(Item):

    def updateDefinitions(self):
        self.definitions = []
        self.relatedWords = []
        self.examples = []

        parser = WiktionaryParser()
        word = parser.fetch(self.lemma, 'english')
        parser.set_default_language('english')
        parser.include_part_of_speech(self.partOfSpeech)

        # merge definition lists of all etymologies
        definitions = []
        for etymology in word:
            defs = etymology.get('definitions', [])
            definitions += defs
        parser.session.close()
        if len(definitions) == 0:
            return

        posWik = self.getPartOfSpeechWiktionaryStyle()
        for definition in definitions:
            pos = definition.get('partOfSpeech', '')
            if pos.lower() == posWik:
                self.definitions = definition['text'][1:]
                self.relatedWords = definition['relatedWords']
                self.examples = definition['examples']
                return

    # https://spacy.io/api/annotation#pos-en
    # to
    # https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech
    def getPartOfSpeechWiktionaryStyle(self):
        mappings = {
            'PROPN': 'noun',
            'ADJ': 'adjective',
            'NOUN': 'noun',
            'VERB': 'verb',
            'ADV': 'adverb',
            'INTJ': 'interjection',
        }
        return mappings.get(self.partOfSpeech, self.partOfSpeech)

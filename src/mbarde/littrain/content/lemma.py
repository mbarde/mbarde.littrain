# -*- coding: utf-8 -*-
from mbarde.littrain import _
from mbarde.littrain.wiktionary import adverbToAdjcetive
from mbarde.littrain.wiktionary import getDefinitions
from mbarde.littrain.wiktionary import getPartOfSpeechWiktionaryStyle
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from z3c.relationfield import RelationChoice
from z3c.relationfield import RelationList
from zope import schema
from zope.interface import implementer

import json


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

    definitions = JSONField(
        title=_(u'Definitions'),
        required=False,
    )

    relatedWords = JSONField(
        title=_(u'Related words'),
        required=False,
    )

    examples = JSONField(
        title=_(u'Examples'),
        required=False,
    )


@implementer(ILemma)
class Lemma(Item):

    def updateDefinitions(self):
        self.definitions = []
        self.relatedWords = []
        self.examples = []

        if self.partOfSpeech == 'ADV':
            # convert adverb lemma to corresponding adjective,
            # since adjectives usually have more detailed definitions
            lemmaAdj = adverbToAdjcetive(self.lemma)
            if lemmaAdj is not False:
                self.lemma = lemmaAdj
                self.partOfSpeech = 'ADJ'

        definitions = getDefinitions(self.lemma)

        if len(definitions) == 0:
            return

        # if Wiktionary does offer only one definition,
        # we use this without further checks
        if len(definitions) == 1:
            self.storeWiktionaryDefinition(definitions[0])
            return

        # otherwise try to find correct definition
        # based on part of speech
        posWik = getPartOfSpeechWiktionaryStyle(self.partOfSpeech)
        for definition in definitions:
            pos = definition.get('partOfSpeech', '')
            if pos.lower() == posWik:
                self.storeWiktionaryDefinition(definition)
                return

    def storeWiktionaryDefinition(self, wikDef):
        self.definitions = json.dumps(wikDef['text'][1:])
        self.relatedWords = json.dumps(wikDef['relatedWords'])
        self.examples = json.dumps(wikDef['examples'])

# -*- coding: utf-8 -*-
from mbarde.littrain import _
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.relationfield import RelationChoice
from z3c.relationfield import RelationList
from zope import schema
from zope.interface import implementer

import json
import urllib2


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


@implementer(ILemma)
class Lemma(Item):

    def updateDefinitions(self):
        apiKey = ''
        url = 'https://api.wordnik.com/v4/word.json/{0}/definitions?limit=200&includeRelated=false&useCanonical=false&includeTags=false&api_key={1}'  # noqa: E501
        url = url.format(self.lemma, apiKey)
        response = urllib2.urlopen(url)
        data = response.read()
        defintions = json.loads(data)

        for definition in defintions:
            partOfSpeechWordnik = definition.get('partOfSpeech', None)
            if partOfSpeechWordnik is not None:
                print('{0}: {1} => {2}'.format(  # noqa: T001
                      self.lemma, self.partOfSpeech, partOfSpeechWordnik))

    def partOfSpeechSpacy2Wordnik(self, partOfSpeechSpacy):
        # https://developer.wordnik.com/docs#!/word/getDefinitions
        # to
        # https://spacy.io/usage/linguistic-features
        mappings = {
            'ADJ': ['adjective'],
            'ADV': ['adverb'],
            'NOUN': ['noun', 'proper-noun-plural', 'proper-noun-posessive'],
            'PROPN': ['proper noun'],
            'VERB': ['verb', 'auxiliary verb', 'transitive verb', 'intransitive verb',
                     'phrasal verb'],
        }
        return mappings(partOfSpeechSpacy)

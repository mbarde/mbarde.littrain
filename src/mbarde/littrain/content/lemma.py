# -*- coding: utf-8 -*-
from mbarde.littrain import _
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.content import Item
from plone.supermodel import model
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


@implementer(ILemma)
class Lemma(Item):
    """
    """

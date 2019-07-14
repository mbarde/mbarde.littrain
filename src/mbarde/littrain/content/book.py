# -*- coding: utf-8 -*-
from mbarde.littrain import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IBook(model.Schema):

    author = schema.TextLine(
        title=_(u'Author'),
        required=True,
    )


@implementer(IBook)
class Book(Container):
    """
    """

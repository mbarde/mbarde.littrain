# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IBook(model.Schema):
    """
    """


@implementer(IBook)
class Book(Container):
    """
    """

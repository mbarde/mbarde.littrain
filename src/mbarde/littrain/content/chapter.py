# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IChapter(model.Schema):
    """
    """


@implementer(IChapter)
class Chapter(Container):
    """
    """

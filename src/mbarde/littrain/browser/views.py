# -*- coding: utf-8 -*-
from mbarde.littrain.epub import EPubReader
from Products.Five.browser import BrowserView

import sys


reload(sys)
sys.setdefaultencoding('utf8')


class ReadEPubView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getChapters(self):
        if self.context.portal_type != 'File':
            return []
        self.ePubReader = EPubReader(self.context.file)
        return self.ePubReader.getChapters()

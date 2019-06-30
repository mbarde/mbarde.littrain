# -*- coding: utf-8 -*-
# from mbarde.littrain.epub import EPubReader
from mbarde.littrain.epub import EPubReader
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa: E501

import os.path
import unittest


def dummy_epub(filename=u'alice.epub'):
    from plone.namedfile.file import NamedBlobImage
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, 'rb') as f:
        file_data = f.read()
    return NamedBlobImage(
        data=file_data,
        filename=filename,
    )


class EPubUnitTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_read(self):
        ePubReader = EPubReader(dummy_epub())
        chapters = ePubReader.getChapters()
        self.assertEqual(len(chapters), 12)
        self.assertEqual(chapters[0]['title'], u'I. Down the Rabbit-Hole')

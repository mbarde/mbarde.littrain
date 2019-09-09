# -*- coding: utf-8 -*-
# from mbarde.littrain.epub import EPubReader
from mbarde.littrain.epub import EPubReader
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.i18n.normalizer import idnormalizer

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
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    def test_read(self):
        ePubReader = EPubReader(dummy_epub())
        chapters = ePubReader.getChapters()
        self.assertEqual(len(chapters), 12)
        self.assertEqual(chapters[0]['title'], u'I. Down the Rabbit-Hole')

        title = chapters[0]['title']
        id = idnormalizer.normalize(title)
        self.assertEqual(chapters[0]['id'], id)

    def test_read_epub_view(self):
        data = {
            'file': dummy_epub(),
        }
        file = api.content.create(
            type='File',
            container=self.portal,
            title=u"Alice's Adventures in Wonderland",
            **data  # noqa: C815
        )

        # test read view:
        path = '/'.join(file.getPhysicalPath() + ('read-epub',))
        view = self.portal.restrictedTraverse(path)
        self.assertTrue(view)
        viewHTML = view()
        self.assertTrue(u'I. Down the Rabbit-Hole' in viewHTML)

# -*- coding: utf-8 -*-
from mbarde.littrain.content.chapter import IChapter  # NOQA E501
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ChapterIntegrationTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Book',
            self.portal,
            'chapter',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_chapter_schema(self):
        fti = queryUtility(IDexterityFTI, name='Chapter')
        schema = fti.lookupSchema()
        self.assertEqual(IChapter, schema)

    def test_ct_chapter_fti(self):
        fti = queryUtility(IDexterityFTI, name='Chapter')
        self.assertTrue(fti)

    def test_ct_chapter_factory(self):
        fti = queryUtility(IDexterityFTI, name='Chapter')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IChapter.providedBy(obj),
            u'IChapter not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_chapter_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Chapter',
            id='chapter',
        )

        self.assertTrue(
            IChapter.providedBy(obj),
            u'IChapter not provided by {0}!'.format(
                obj.id,
            ),
        )

        # check that deleting the object works too
        self.assertIn('chapter', self.parent.objectIds())
        api.content.delete(obj=obj)
        self.assertNotIn('chapter', self.parent.objectIds())

    def test_ct_chapter_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Chapter')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id),
        )

    def test_ct_chapter_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Chapter')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'chapter_id',
            title='Chapter container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )

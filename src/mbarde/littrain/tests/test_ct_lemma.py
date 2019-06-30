# -*- coding: utf-8 -*-
from mbarde.littrain.content.lemma import ILemma  # NOQA E501
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class LemmaIntegrationTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_lemma_schema(self):
        fti = queryUtility(IDexterityFTI, name='Lemma')
        schema = fti.lookupSchema()
        self.assertEqual(ILemma, schema)

    def test_ct_lemma_fti(self):
        fti = queryUtility(IDexterityFTI, name='Lemma')
        self.assertTrue(fti)

    def test_ct_lemma_factory(self):
        fti = queryUtility(IDexterityFTI, name='Lemma')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ILemma.providedBy(obj),
            u'ILemma not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_lemma_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Lemma',
            id='lemma',
        )

        self.assertTrue(
            ILemma.providedBy(obj),
            u'ILemma not provided by {0}!'.format(
                obj.id,
            ),
        )

        # check that deleting the object works too
        self.assertIn('lemma', self.portal.objectIds())
        api.content.delete(obj=obj)
        self.assertNotIn('lemma', self.portal.objectIds())

    def test_ct_lemma_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Lemma')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id),
        )

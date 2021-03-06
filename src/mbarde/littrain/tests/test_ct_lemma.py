# -*- coding: utf-8 -*-
from mbarde.littrain.content.lemma import ILemma  # NOQA E501
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa
from mbarde.littrain.utils import getUsersLearnedLemmas
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
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
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Chapter',
            self.portal,
            'chapter',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

        self.SECOND_TEST_USER_NAME = 'second-test-user'
        api.user.create(
            email=self.SECOND_TEST_USER_NAME + '@test.org',
            username=self.SECOND_TEST_USER_NAME,
        )

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
            container=self.parent,
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
        self.assertIn('lemma', self.parent.objectIds())
        api.content.delete(obj=obj)
        self.assertNotIn('lemma', self.parent.objectIds())

    def test_ct_lemma_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Lemma')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id),
        )

    def test_lemma_wrong_part_of_speech(self):
        lemma = api.content.create(
            container=self.parent,
            type='Lemma',
            id='lemma',
        )
        lemma.partOfSpeech = 'ADV'
        lemma.lemma = 'closer'
        lemma.updateDefinitions()
        self.assertTrue(len(lemma.definitions) > 0)
        self.assertEqual(lemma.partOfSpeech, 'ADJ')

    def test_lemma_set_state_for_user(self):
        learnedLemmas = getUsersLearnedLemmas()
        self.assertEqual(len(learnedLemmas), 0)

        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        lemma = api.content.create(
            container=self.parent,
            type='Lemma',
            id='lemma',
        )

        self.assertFalse(lemma.isLearnedByCurrentUser())
        lemma.setAsLearnedForCurrentUser()
        self.assertTrue(lemma.isLearnedByCurrentUser())
        logout()

        login(self.portal, self.SECOND_TEST_USER_NAME)
        self.assertFalse(lemma.isLearnedByCurrentUser())
        lemma.setAsLearnedForCurrentUser()
        self.assertTrue(lemma.isLearnedByCurrentUser())
        logout()

        login(self.portal, TEST_USER_NAME)
        self.assertTrue(lemma.isLearnedByCurrentUser())
        lemma.setAsNotLearnedForCurrentUser()
        self.assertFalse(lemma.isLearnedByCurrentUser())

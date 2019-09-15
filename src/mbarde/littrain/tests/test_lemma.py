# -*- coding: utf-8 -*-
from mbarde.littrain.lemma import LemmaCollector
from mbarde.littrain.lemma import LemmaStorer
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa: E501
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import json
import unittest


class LemmaUnitTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_lemma_collector(self):
        chapters = [
            {
                'title': u'Pickle Rick',
                'content': u"[Morty hesitantly picks up the screwdriver and turns the pickle over. The pickle has Rick's face on it] I turned myself into a pickle, Morty! Boom! Big reveal: I'm a pickle. What do you think about that? I turned myself into a pickle! W-what are you just staring at me for, bro. I turned myself into a pickle, Morty!",  # noqa: E501
            },
            {
                'title': u'Rixty Minutes',
                'content': u"Hey, are you tired of real doors, cluttering up your house, where you open 'em, and they actually go somewhere? [music starts] And you go in another room?",  # noqa: E501
            },
        ]

        lemmaCollector = LemmaCollector()
        self.assertEqual(len(lemmaCollector.lemmas), 0)

        chapter = chapters[0]
        lemmaCollector.updateLemmasByChapter(chapter['content'], chapter['title'])
        self.assertEqual(len(lemmaCollector.lemmas), 15)

        chapter = chapters[1]
        lemmaCollector.updateLemmasByChapter(chapter['content'], chapter['title'])
        self.assertEqual(len(lemmaCollector.lemmas), 26)

        self.assertEqual(len(lemmaCollector.getLemmasWithMaxOccurence()), 23)
        self.assertEqual(len(lemmaCollector.getLemmasWithMaxOccurence(10)), 26)

        storer = LemmaStorer('Rickle Pick')
        lemmaCollector.storeLemmas(storer)

        self.assertEqual(self.portal.books.portal_type, 'Folder')
        self.assertEqual(len(self.portal.books.listFolderContents()), 1)

        book = self.portal.books.listFolderContents()[0]
        self.assertEqual(book.portal_type, 'Book')
        self.assertEqual(book.id, 'rickle-pick')
        self.assertEqual(book.title, 'Rickle Pick')

        self.assertEqual(len(book.listFolderContents()), len(chapters))
        chapter = book.listFolderContents()[1]
        self.assertEqual(chapter.portal_type, 'Chapter')
        self.assertEqual(chapter.id, 'rixty-minutes')
        self.assertEqual(chapter.title, chapters[1]['title'])

        self.assertEqual(len(chapter.listFolderContents()), 11)
        lemma = chapter.listFolderContents()[1]
        self.assertEqual(lemma.lemma, u'tired')
        self.assertEqual(lemma.count, 1)
        self.assertEqual(len(lemma.chapters), 1)
        self.assertEqual(lemma.chapters[0].to_object, chapter)
        self.assertEqual(lemma.partOfSpeech, 'ADJ')

        # test lemma view:
        path = '/'.join(lemma.getPhysicalPath() + ('view',))
        view = self.portal.restrictedTraverse(path)
        self.assertTrue(view)
        viewHTML = view()
        self.assertTrue(u'tired' in viewHTML)

        lemma.updateDefinitions()
        self.assertTrue('In need of some rest' in lemma.definitions)
        self.assertTrue('fatigued' in lemma.relatedWords)
        self.assertTrue('tired of this' in lemma.examples)

        chapter0 = book.listFolderContents()[0]
        chapter1 = book.listFolderContents()[1]
        self.assertEqual(len(chapter0.listFolderContents()) +
                         len(chapter1.listFolderContents()), 26)

        # test adverb definitions
        lemma = chapter0.listFolderContents()[1]
        self.assertEqual(lemma.lemma, 'hesitantly')
        self.assertEqual(lemma.partOfSpeech, 'ADV')
        lemma.updateDefinitions()
        self.assertEqual(lemma.partOfSpeech, 'ADJ')
        self.assertEqual(lemma.lemma, 'hesitant')
        definitions = json.loads(lemma.definitions)
        self.assertTrue(len(definitions) > 0)

        storer = LemmaStorer('Rickle Pick - Occurence One')
        lemmaCollector.storeLemmas(storer, maxOccurence=1)
        book = self.portal.books.listFolderContents()[1]
        self.assertEqual(book.portal_type, 'Book')
        self.assertEqual(book.id, 'rickle-pick-occurence-one')
        self.assertEqual(book.title, 'Rickle Pick - Occurence One')
        chapter0 = book.listFolderContents()[0]
        chapter1 = book.listFolderContents()[1]
        self.assertEqual(len(chapter0.listFolderContents()) +
                         len(chapter1.listFolderContents()), 23)

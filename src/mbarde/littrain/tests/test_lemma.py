# -*- coding: utf-8 -*-
from mbarde.littrain.lemma import LemmaCollector
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa: E501

import unittest


class LemmaUnitTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

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
        self.assertEqual(len(lemmaCollector.lemmas), 27)

# -*- coding: utf-8 -*-
# from mbarde.littrain.epub import EPubReader
from mbarde.littrain.testing import MBARDE_LITTRAIN_INTEGRATION_TESTING  # noqa: E501

import unittest


class LemmaUnitTest(unittest.TestCase):

    layer = MBARDE_LITTRAIN_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_read(self):
        pass

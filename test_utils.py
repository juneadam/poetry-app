#testing utilities
import os
from unittest import TestCase
import unittest
from server import app
from flask import session
from functools import wraps
import utils

class FlaskTestsUtilsPayload(TestCase):
    """Tests utility functions."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_get_payload_4params(self):

        assert utils.get_payload(author="shakespeare", title="sonnet", lines="thence", linecount="14") == ('author,title,lines,linecount','shakespeare;sonnet;thence;14')
    
    def test_get_payload_2params(self):

        assert utils.get_payload(author="byron", linecount="20") == ('author,linecount','byron;20')

    def test_get_payload_0params(self):

        assert utils.get_payload() == ('','')


class FlaskTestsUtilsLogicFuncs(TestCase):
    """Tests utility functions."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_range_modifier(self):

        for linecount in range(1,4):
            assert utils.range_modifier(linecount) == 5
        for linecount in range(4,10):
            assert utils.range_modifier(linecount) == 2

    def test_form_easter_egg(self):

        assert utils.form_easter_egg(3) == "Haiku: "
        assert utils.form_easter_egg(5) == "Limerick: "
        assert utils.form_easter_egg(14) == "Sonnet: "
        assert utils.form_easter_egg(19) == "Villanelle: "
        assert utils.form_easter_egg(100) == "Cento: "


if __name__ == "__main__":
    unittest.main()

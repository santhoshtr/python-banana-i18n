"""Test i18n module."""
#
# (C) 2007-2019, Pywikibot team
# (C) 2020 Kunal Mehta <legoktm@member.fsf.org>
#
# Distributed under the terms of the MIT license.
#

import os
import unittest

from banana_i18n import BananaI18n, plural


class TestTWTranslate(unittest.TestCase):

    """Test translate method."""

    def setUp(self) -> None:
        self.i18n = BananaI18n(os.path.join(os.path.dirname(__file__), 'i18n'))

    def testLocalized(self):
        """Test fully localized entry."""
        self.assertEqual(self.i18n.translate('en', 'test-localized'),
                         'test-localized EN')
        self.assertEqual(self.i18n.translate('nl', 'test-localized'),
                         'test-localized NL')
        self.assertEqual(self.i18n.translate('fy', 'test-localized'),
                         'test-localized FY')

    def testSemiLocalized(self):
        """Test translating with fallback to alternative language."""
        self.assertEqual(self.i18n.translate('en', 'test-semi-localized'),
                         'test-semi-localized EN')
        self.assertEqual(self.i18n.translate('nl', 'test-semi-localized'),
                         'test-semi-localized NL')
        # Falls back to nl
        self.assertEqual(self.i18n.translate('srn', 'test-semi-localized'),
                         'test-semi-localized NL')

    def testNonLocalized(self):
        """Test translating non localized entries."""
        self.assertEqual(self.i18n.translate('en', 'test-non-localized'),
                         'test-non-localized EN')
        self.assertEqual(self.i18n.translate('fy', 'test-non-localized'),
                         'test-non-localized EN')
        self.assertEqual(self.i18n.translate('nl', 'test-non-localized'),
                         'test-non-localized EN')
        self.assertEqual(self.i18n.translate('ru', 'test-non-localized'),
                         'test-non-localized EN')

    def testKnownLanguages(self):
        self.assertEqual(self.i18n.known_languages(), ['de', 'en', 'fr', 'fy', 'ja', 'nl'])


class TestTWNTranslate(unittest.TestCase):
    """Test {{PLURAL:}} support."""
    def setUp(self) -> None:
        self.i18n = BananaI18n(os.path.join(os.path.dirname(__file__), 'i18n'))

    @unittest.expectedFailure
    def testNumber(self):
        """Use a number."""
        self.assertEqual(
            self.i18n.translate('de', 'test-plural', 0) % {'num': 0},
            'Bot: Ändere 0 Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-plural', 1) % {'num': 1},
            'Bot: Ändere 1 Seite.')
        self.assertEqual(
            self.i18n.translate('de', 'test-plural', 2) % {'num': 2},
            'Bot: Ändere 2 Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-plural', 3) % {'num': 3},
            'Bot: Ändere 3 Seiten.')
        self.assertEqual(
            self.i18n.translate('en', 'test-plural', 0) % {'num': 'no'},
            'Bot: Changing no pages.')
        self.assertEqual(
            self.i18n.translate('en', 'test-plural', 1) % {'num': 'one'},
            'Bot: Changing one page.')
        self.assertEqual(
            self.i18n.translate('en', 'test-plural', 2) % {'num': 'two'},
            'Bot: Changing two pages.')
        self.assertEqual(
            self.i18n.translate('en', 'test-plural', 3) % {'num': 'three'},
            'Bot: Changing three pages.')

    def testDict(self):
        """Use a dictionary."""
        self.assertEqual(
            self.i18n.translate('en', 'test-plural', {'num': 2}),
            'Bot: Changing 2 pages.')

    def testExtended(self):
        """Use additional format strings."""
        self.assertEqual(
            self.i18n.translate('fr', 'test-plural',
                                {'num': 1, 'descr': 'seulement'}),
            'Robot: Changer seulement une page.')

    @unittest.expectedFailure
    def testExtendedOutside(self):
        """Use additional format strings also outside."""
        self.assertEqual(
            self.i18n.translate('fr', 'test-plural', 1) % {'descr': 'seulement'},
            'Robot: Changer seulement une page.')

    def testMultiple(self):
        """Test using multiple plural entries."""
        """
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', 1)
            % {'action': 'Ändere', 'line': 'eine'},
            'Bot: Ändere eine Zeile von einer Seite.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', 2)
            % {'action': 'Ändere', 'line': 'zwei'},
            'Bot: Ändere zwei Zeilen von mehreren Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', 3)
            % {'action': 'Ändere', 'line': 'drei'},
            'Bot: Ändere drei Zeilen von mehreren Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', (1, 2, 2))
            % {'action': 'Ändere', 'line': 'eine'},
            'Bot: Ändere eine Zeile von mehreren Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', [3, 1, 1])
            % {'action': 'Ändere', 'line': 'drei'},
            'Bot: Ändere drei Zeilen von einer Seite.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', ['3', 1, 1])
            % {'action': 'Ändere', 'line': 'drei'},
            'Bot: Ändere drei Zeilen von einer Seite.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals', '321')
            % {'action': 'Ändere', 'line': 'dreihunderteinundzwanzig'},
            'Bot: Ändere dreihunderteinundzwanzig Zeilen von mehreren Seiten.')
        """
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals',
                                {'action': 'Ändere', 'line': 1, 'page': 1}),
            'Bot: Ändere 1 Zeile von einer Seite.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals',
                                {'action': 'Ändere', 'line': 1, 'page': 2}),
            'Bot: Ändere 1 Zeile von mehreren Seiten.')
        self.assertEqual(
            self.i18n.translate('de', 'test-multiple-plurals',
                                {'action': 'Ändere', 'line': 11, 'page': 2}),
            'Bot: Ändere 11 Zeilen von mehreren Seiten.')

    def testMultipleWrongParameterLength(self):
        """Test wrong parameter length."""
        err_msg = 'Length of parameter does not match PLURAL occurrences'
        with self.assertRaisesRegex(ValueError, err_msg):
            self.i18n.translate('de', 'test-multiple-plurals', {'action': 1, 'line': 2})

        with self.assertRaisesRegex(ValueError, err_msg):
            self.i18n.translate('de', 'test-multiple-plurals', {'action': 123})

    def testMultipleNonNumbers(self):
        """Test error handling for multiple non-numbers."""
        with self.assertRaisesRegex(
            TypeError, r"type <class 'str'> for value line \(drei\)"
        ):
            self.i18n.translate('de', 'test-multiple-plurals',
                                {'action': 1, 'line': 'drei', 'page': 1})
        with self.assertRaisesRegex(
            TypeError, r"type <class 'str'> for value line \(elf\)"
        ):
            self.i18n.translate('de', 'test-multiple-plurals',
                                {'action': 'Ändere', 'line': 'elf', 'page': 2})

    def testAllParametersExist(self):
        """Test that all parameters are required when using a dict."""
        # all parameters must be inside twntranslate
        self.assertEqual(self.i18n.translate('de', 'test-multiple-plurals',
                                             {'line': 1, 'page': 1}),
                         'Bot: %(action)s %(line)s Zeile von einer Seite.')

    @unittest.expectedFailure
    def test_fallback_lang(self):
        """
        Test that twntranslate uses the translation's language.

        twntranslate calls _twtranslate which might return the translation for
        a different language and then the plural rules from that language need
        to be applied.
        """
        # co has fr as altlang but has no plural rules defined (otherwise this
        # test might not catch problems) so it's using the plural variant for 0
        # although French uses the plural variant for numbers > 1 (so not 0)
        assert 'co' not in plural.plural_rules
        assert plural.plural_rules['fr']['plural'](0) is False
        self.assertEqual(
            self.i18n.translate('co', 'test-plural',
                                {'num': 0, 'descr': 'seulement'}),
            'Robot: Changer seulement une page.')
        self.assertEqual(
            self.i18n.translate('co', 'test-plural',
                                {'num': 1, 'descr': 'seulement'}),
            'Robot: Changer seulement une page.')


class TestExtractPlural(unittest.TestCase):

    """Test extracting plurals from a dummy string."""

    def setUp(self) -> None:
        self.i18n = BananaI18n('not-real-directory')

    net = False

    def test_standard(self):
        """Test default usage using a dict and no specific plurals."""
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|other}}',
                                      {'foo': 42}),
            'other')
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|other}}',
                                      {'foo': 1}),
            'one')
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|other}}',
                                      {'foo': 0}),
            'other')

    def test_empty_fields(self):
        """Test default usage using a dict and no specific plurals."""
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo||other}}', {'foo': 42}),
            'other')
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo||other}}', {'foo': 1}),
            '')
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|}}', {'foo': 1}),
            'one')

        # two variants expected but only one given
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one}}', {'foo': 0}),
            'one')

    def test_specific(self):
        """Test using a specific plural."""
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|other|12=dozen}}',
                                      {'foo': 42}),
            'other')
        self.assertEqual(
            self.i18n._extract_plural('en', '{{PLURAL:foo|one|other|12=dozen}}',
                                      {'foo': 12}),
            'dozen')

    def test_more(self):
        """Test the number of plurals are more than expected."""
        test = [(0, 2), (1, 0), (2, 1), (3, 2), (4, 2), (7, 2), (8, 3)]
        for num, result in test:
            self.assertEqual(
                self.i18n._extract_plural(
                    'cy',
                    '{{PLURAL:num|0|1|2|3|4|5}}',
                    {'num': num}),
                str(result))

    def test_less(self):
        """Test the number of plurals are less than expected."""
        test = [(0, 2), (1, 0), (2, 1), (3, 2), (4, 2), (7, 2), (8, 3)]
        for num, result in test:
            self.assertEqual(
                self.i18n._extract_plural(
                    'cy',
                    '{{PLURAL:num|0|1}}',
                    {'num': num}),
                str(min(result, 1)))

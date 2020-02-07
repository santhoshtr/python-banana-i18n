"""
Various i18n functions.

Helper functions for both the internal translation system
and for TranslateWiki-based translations.
"""
#
# (C) 2004-2019 Pywikibot team
# (C) 2020 Kunal Mehta <legoktm@member.fsf.org>
#
# Distributed under the terms of the MIT license.
#
from collections import defaultdict
from collections.abc import Mapping
import json
import os
from pathlib import Path
import re
from typing import DefaultDict, Dict, List, Union

from .plural import plural_rule

PLURAL_PATTERN = r'{{PLURAL:(?:%\()?([^\)]*?)(?:\)d)?\|(.*?)}}'


class BananaI18n:
    def __init__(self, messagesdir: Union[str, Path]):
        self.messagesdir = Path(messagesdir)
        self.cache = defaultdict(dict)  # type: DefaultDict[str, Dict[str, Union[str, None]]]

    def _get_translation(self, lang: str, twtitle: str) -> Union[str, None]:
        try:
            return self.cache[lang][twtitle]
        except KeyError:
            pass
        fname = self.messagesdir / '{}.json'.format(lang)
        try:
            with fname.open() as f:
                transdict = json.load(f)
        except (OSError, IOError):  # file open can cause several exceptions
            self.cache[lang][twtitle] = None
            return None
        self.cache[lang].update(transdict)
        try:
            return transdict[twtitle]
        except KeyError:
            return None

    def _get_fallbacks_for(self, lang: str) -> List[str]:
        with open(os.path.join(os.path.dirname(__file__), 'fallback.json')) as f:
            return json.load(f).get(lang, [])

    def _extract_plural(self, lang: str, message: str, parameters: Mapping) -> str:
        """Check for the plural variants in message and replace them.

        @param message: the message to be replaced
        @param parameters: plural parameters passed from other methods
        @type parameters: Mapping of str to int
        @return: The message with the plural instances replaced
        """
        def static_plural_value(n):
            return rule['plural']

        def replace_plural(match):
            selector = match.group(1)
            variants = match.group(2)
            try:
                num = parameters[selector]
            except KeyError:
                raise ValueError(
                    "Length of parameter does not match PLURAL occurrences in {}"
                    .format(message)
                )
            if not isinstance(num, (int, float)):
                raise TypeError(
                    'type {0} for value {1} ({2})'
                    .format(type(num), selector, num))

            plural_entries = []
            specific_entries = {}
            # A plural entry can not start at the end of the variants list,
            # and must end with | or the end of the variants list.
            for number, plural in re.findall(
                r'(?!$)(?: *(\d+) *= *)?(.*?)(?:\||$)', variants
            ):
                if number:
                    specific_entries[int(number)] = plural
                else:
                    assert not specific_entries, (
                        'generic entries defined after specific in "{0}"'
                        .format(variants))
                    plural_entries += [plural]

            if num in specific_entries:
                return specific_entries[num]

            index = plural_value(num)
            needed = rule['nplurals']
            if needed == 1:
                assert index == 0

            if index >= len(plural_entries):
                # take the last entry in that case, see
                # https://translatewiki.net/wiki/Plural#Plural_syntax_in_MediaWiki
                index = -1
            return plural_entries[index]

        assert isinstance(parameters, Mapping), \
            'parameters is not Mapping but {0}'.format(type(parameters))
        rule = plural_rule(lang)
        plural_value = rule['plural']
        if not callable(plural_value):
            assert rule['nplurals'] == 1
            plural_value = static_plural_value

        return re.sub(PLURAL_PATTERN, replace_plural, message)

    def translate(self, lang: str, twtitle: str, parameters: Mapping = None,
                  fallback=True) -> Union[str, None]:
        """Return the most appropriate translation from a translation dict.

        Given a language code and a dictionary, returns the dictionary's value for
        key 'code' if this key exists; otherwise tries to return a value for an
        alternative language that is most applicable to use on the wiki in
        language 'code' except fallback is False.

        The language itself is always checked first, then languages that
        have been defined to be alternatives, and finally English. If none of
        the options gives result, we just take the one language from xdict which
        may not be always the same. When fallback is iterable it'll return None if
        no code applies (instead of returning one).

        :raises IndexError: If the language supports and requires more plurals than
            defined for the given translation template.
        """
        # Get the translated string
        langs = [lang]
        if fallback:
            langs += self._get_fallbacks_for(lang)
        for try_lang in langs:
            trans = self._get_translation(try_lang, twtitle)
            if trans is not None:
                # We got something
                break
        if trans is None:
            return None  # return None if we have no translation found
        if parameters is None:
            return trans

        plural_parameters = parameters

        # else we check for PLURAL variants
        trans = self._extract_plural(try_lang, trans, plural_parameters)
        if parameters:
            try:
                return trans % parameters
            except (KeyError, TypeError):
                # parameter is for PLURAL variants only, don't change the string
                pass
        return trans

    def known_languages(self) -> List[str]:
        """All languages we have localizations for"""
        langs = []
        for fname in self.messagesdir.iterdir():
            if fname.suffix == '.json':
                langs.append(fname.stem)

        return sorted(langs)

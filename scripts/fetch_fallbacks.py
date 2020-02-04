"""
Fetch language fallback map from MediaWiki
"""
#
# (C) 2020 Kunal Mehta <legoktm@member.fsf.org>
#
# Distributed under the terms of the MIT license.

from collections import defaultdict
import json
import os
import requests


def main():
    req = requests.get('https://meta.wikimedia.org/w/api.php', params={
        "action": "query",
        "meta": "languageinfo",
        "liprop": "fallbacks",
        "format": "json",
        "formatversion": "2",
    })
    req.raise_for_status()
    data = req.json()
    assert data['batchcomplete'] is True
    langs = data['query']['languageinfo']
    mapping = defaultdict(list)
    for lang, info in langs.items():
        if info['fallbacks']:
            mapping[lang] = info['fallbacks']
        if lang != 'en' and 'en' not in mapping[lang]:
            # Everything must fallback to en eventually
            mapping[lang].append('en')

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'banana_i18n/fallback.json')
    with open(path, 'w') as f:
        json.dump(mapping, f, indent='    ')
    print('Updated {}'.format(path))


if __name__ == '__main__':
    main()

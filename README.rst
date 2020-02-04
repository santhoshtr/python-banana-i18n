banana-i18n
===========

A localization library for Python based on the banana_ message file format.
This library was originally developed inside of Pywikibot_ and then forked
into a separate library for easier reuse.

Message specification
---------------------
For the most part we use the upstream banana file format, with a few Python
tweaks.

Parameters to messages are specified through printf-style formatting::

    "bot-change-page": "Bot: Changing %(num)s {{PLURAL:%(num)d|page|pages}}.",

All parameters are named. Gender, grammar, and bidi support has not yet been
implemented.

Usage
-----
Assuming the directory with your JSON files is named ``i18n``::

    from banana_i18n import BananaI18n

    banana = BananaI18n('i18n')
    text = banana.translate('de', 'example')

Parameters must be passed as a dictionary::

    text = banana.translate('de', 'bot-change-page', {'num': 2})

If the parameter is going to be used in ``{{PLURAL:}}``, it must be the ``int``
type.

A list of all localized languages can be accesssed through
``banana.known_languages()``.

License
-------
banana-i18n is available under the terms of the MIT license.

* \(C) 2004-2019 Pywikibot team
* \(C) 2011-2017 xqt
* \(C) 2020 Kunal Mehta <legoktm@member.fsf.org>


.. _banana: https://github.com/wikimedia/banana-i18n#banana-file-format
.. _Pywikibot: https://www.mediawiki.org/wiki/Manual:Pywikibot

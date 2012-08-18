reStructuredText Tools
======================
:author: Tadhg O’Higgins
:date: 2012-03-26

This is a small collection of tools intended to aid in writing reStructuredText. All of the Vim functionality relies on the filetype being ``rest`` rather than the typical ``rst``.

The |rest_get_refs.py|_ script can be used on its own, but the other parts are meant to be installed as a `pathogen`_ bundle, by executing this from your ``bundles`` directory: ``git clone git://github.com/erisian/rest_tools.git rest_tools``.

Why?
----

So that to write the following::

    Heading
    -------
    I want a `“link that's quoted”`_, followed by a footnote\ [#]_, then a list:

    +   Item one—verily!
    +   Item two includes a link to |Hamlet|_.
    +   Item three includes **strength**.
    +   Item four is a tennis score: 6–3, 6–4.
    +   Item five has simple math: 54−49.

I typed::

    Heading
    h2<Tab>
    I want a lq<Tab>link that's quoted<Tab>, followed by a footnote;n, then a list:

    i<Tab>Item one--verily!
    i<Tab>Item two includes a link to lct<Tab>Hamlet<Tab>.
    i<Tab>Item three includes s<Tab>strength<Tab>.
    i<Tab>Item four is a tennis score: 6;d3, 6;d4.
    i<Tab>Item five has simple math: 54;m49.

And to add the reference definitions at the end::

    .. |Hamlet| replace:: `Hamlet`
    .. _Hamlet:
    .. _“link that's quoted”: 
    .. [#] 

I just filtered the file through the |rest_get_refs.py|_ script by executing ``:Grefs``.

Components
----------
|rest_get_refs.py|_
    Goes through a reStructuredText document and looks at all link, footnote, and substitution references, then places their corresponding definitions at the end, eliminating otherwise tedious repetition.
`reStructuredText Snippets`_
    These depend on the excellent `snipMate.vim`_ plugin, and define snippets for various common reStructuredText constructs.
`reStructuredText Shortcuts`_
    These are all insert mode key combinations, primarily relying on the semi-colon as a “leader” key. For example, ``;n`` produces ``\ [#]_``.
`reStructuredText Surrounds`_
    These depend on the excellent `surround.vim`_ plugin, and define shortcut keys for that plugin used for common reStructuredText constructs. For example, ``yswl`` makes the current word into a reStructuredText link.
`reStructuredText Syntax`_
    An alternative to the existing syntax files that I happen to prefer.

I write all of my reStructuredText in Unicode, saving it as UTF-8, and frequently use common non-ASCII characters. The following tools are currently part of the overall reStructuredText toolkit presented here, but could theoretically be split out and used in any Unicode document format:

`Unicode Snippets`_
    These depend on the excellent `snipMate.vim`_ plugin, and provide easier ways to type common non-ASCII characters. For example, ``q<Tab>`` wraps the cursor in curly double quotation marks.
`Unicode Shortcuts`_
    These are all insert mode key combinations, primarily relying on the semi-colon as a “leader” key. For example, ``;e`` produces ``€``.
`Unicode Surrounds`_
    These depend on the excellent `surround.vim`_ plugin, and define shortcut keys for that plugin used for common Unicode characters. For example, ``yswq`` wraps the current word with curly double quotation marks.
`Unicode Syntax`_
    My reStructuredText syntax includes highlighting for a number of non-reStructuredText syntax, including quoted text, parenthetical text, and various kinds of dashes, which has proven useful in preventing various silly errors (like forgetting to close a parenthetical aside).

``rest_get_refs.py``
--------------------
This is a standalone Python file. I include a Vim command, ``Grefs``, to invoke it from within Vim. By default ``Grefs`` runs against the entire file, but it can also be run using the standard Vim ranges.

It requires at least Python 2.6, although it would be fairly easy to support older versions if there were any demand. Run from the command line without arguments, it takes standard input and returns standard output. Alternatively, ``-f`` specifies a file to read from, and ``-d`` specifies a file to write to.

It will look for link, footnote, substitution, and substitution/link references, and add syntax for their definitions to the end of the file. For example, given::

    This is a `link`_; this sentence ends with a footnote\ [#]_.

    Here's a |substitution|, and here's a title that's also a link: |The Dispossessed|_

It will return::

    This is a `link`_; this sentence ends with a footnote\ [#]_.

    Here's a |substitution|, and here's a title that's also a link: |The Dispossessed|_


    .. |The Dispossessed| replace:: `The Dispossessed`
    .. _The Dispossessed:
    .. |substitution| replace:: substitution
    .. _link: 
    .. [#] 

It can be configured to place the reference definitions at a specific point in the file, rather than at the end, and changing the configuration could add support for some additional constructs.

Configuration is handled by a JSON file, ``rest_get_refs.json``, with two sections, ``filetypes`` and ``patterns``. The former governs how the script looks for a marker in the text that determines what kind of file it is, then provides a line above which the definitions will be inserted.

The ``patterns`` section governs how the script's overengineered and somewhat fragile regular expression constructs deal with various kinds of syntax. Each syntax construct is a dictionary with the following keys:

``closer``
    The character(s) that close the syntax construct.
``description``
    A description of the pattern. Optional.
``false_closer``
    A character that matches another pattern but not this one, such as ``|``, which closes a substitution but not a substitution link. Basically a kludge that I need to excise.
``opener``
    The character(s) that open the syntax construct.
``reference_start``
    The start of the reference, e.g. ``\.\. [#]`` for a numeric footnote. Used to determine (not always successfully) whether or not the reference has already been defined.
``reference``
    The reference definition that will be inserted at the bottom, e.g. ``\.\. |{content}| replace:: `{content}`\n.. _{content}:`` for a substitution that is also a link.
``substitute``
    Unless the script should alter the reference in the text itself, this should be absent or set to the JavaScript Boolean ``false``. If present, used to alter the reference; I find this useful in cases where I want to make it easy to insert a specific special role many times.

The one non-standard construct covered by the default configuration is the “special role”; reStructuredText makes it easy to define custom roles, which can then be used to classify terms in the document. Given this input::

    Here's a term that needs ~special~ treatment.

It will return::

    Here's a term that needs |special| treatment.


    .. |special| replace:: :specialrole:`special`

(Note that there must be a ``.. role:: specialrole`` line somewhere in the document before the replacement line, and that the script does not currently insert this for you.)

The easiest way to use it from Vim is simply to use ``Grefs`` in the command line, but you could also call it as a filter, e.g. ``:%!~/.vim/bundle/rest_tools/rest_get_refs/rest_get_refs.py``

reStructuredText Snippets
-------------------------
======= =======================================
``e``   ``*emphasis*``
``s``   ``**strong**``
``c``   ````code````
``t``   ```title```
``l``   ```link`_``
``lq``  ```“quoted link”`_``
``lct`` ``|substitution link|_``
``i``   ``+   list item``
``n``   ``#.  numeric list item``
``fn``  ``[*]_``
``fs``  ``..  [*]``
``nf``  ``[#]_``
``ns``  ``..  [#]``
``pb``  ``class:: page-break\n\n    -----\n\n``
``hr``  ``-----``
======= =======================================

In addition, ``h`` followed by one of the following characters and then ``<Tab>`` will insert as many of those characters as are on the line above: ``+=-#*:``. ``h`` followed by 1 to 6 followed by ``<Tab>`` will insert the same characters, in the order ``=-+*#:`` (this order is arbitrary; reStructuredText only cares about what order they show up in the document).

reStructuredText Shortcuts
--------------------------
====== ==========
``;f`` ``\ [*]_``
``;n`` ``\ [#]_``
====== ==========

reStructuredText Surrounds
--------------------------
===== =============================
``e`` Surround a word with ``*``.
``l`` Surround a word with ````_``.
``s`` Surround a word with ``**``.
===== =============================

reStructuredText Syntax
-----------------------
An alternative to the existing syntax files that I happen to prefer. ``conceallevel=2`` is recommended.

This is a sample of how it looks with my color scheme and ``conceallevel=2``:

.. image:: https://github.com/erisian/rest_tools/raw/master/syntax_conceallevel2.png

This is a sample of how it looks with my color scheme and ``conceallevel=0``:

.. image:: https://github.com/erisian/rest_tools/raw/master/syntax_conceallevel0.png

Unicode Snippets
----------------
====== ===============================
``q``  Double quotation marks: ``“”``.
``Q``  Single quotation marks: ``‘’``.
``rx`` ℞.
====== ===============================

Unicode Shortcuts
-----------------
These are all insert mode shortcuts.

====== =============================
``--`` em dash: ``—``.
``;-`` en dash: ``–``.
``;d`` en dash: ``–``
``;m`` minus sign: ``−``
``;;`` ellipsis: ``…``
``;q`` open double quotation: ``“``

       .. fix syntax: ”
``;Q`` close double quotation: ``”``
``;'`` close single quotation: ``’``
``;o`` bullet dot: ``•``
``;0`` degree symbol: ``°``
``;e`` euro: ``€``
``;r`` rx sign: ``℞``
``;c`` cents: ``¢``
``;l`` pound currency: ``£``
``;t`` therefore: ``∴``
``;C`` copyright: ``©``
``;R`` registered trademark: ``®``
``-_`` down arrow: ``↓``
``->`` right arrow: ``→``
``-^`` up arrow: ``↑``
``-<`` left arrow: ``←``
``-;`` en dash: ``–``
====== =============================

Unicode Surrounds
-----------------
===== ============================
``q`` Surround a word with ``“”``.
===== ============================

Unicode Syntax
--------------
Provides highlighting for:

+   Em dashes.
+   En dashes.
+   Minus signs.
+   Sections in double quotation marks.
+   Sections in single quotation marks.
+   Sections in parentheses.
+   If Vim's ``conceal`` functionality is available, will conceal backslash-space.

.. |rest_get_refs.py| replace:: ``rest_get_refs.py``
.. _pathogen: https://github.com/tpope/vim-pathogen
.. _snipMate.vim: http://www.vim.org/scripts/script.php?script_id=2540
.. _surround.vim: https://github.com/tpope/vim-surround

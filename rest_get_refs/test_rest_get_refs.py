#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
import rest_get_refs

class test_RestGetRefs(object):

    def setUp(self):
        self.rr = rest_get_refs.RSTReferencer()
        self.rr.setup_config()

    def test_functional(self):
        """
            Test it end to end.
        """
        pass

    def test_setup_cli_options(self):
        import sys
        testcases = [
            (
                ["-f", "/foo/bar/foobar.txt"],
                {"sourcefile": "/foo/bar/foobar.txt"}
            )
        ]

        def handle_testcases(testcase):
            sys.argv[1:] = testcase[0]
            self.rr.setup_cli_options()
            assert self.rr.options == testcase[1]

        map(handle_testcases, testcases)

    def test_handle_cli_options(self):
        """
            This looks tricky to test, at least without creating a bunch of
            dummy test files, or mocking stdin.
            Skipping for the moment.
        """
        pass

    def test_determine_filetype(self):
        testcases = [
            {
                #blog
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "filetype": {
                    "marker": ":PostID: [",
                    "insert": ".. container:: date"
                }
            }
        ]

        def handle_testcases(case):
            self.rr.sourcetext = case["text"]
            self.rr.determine_filetype()
            assert self.rr.filetype == case["filetype"]

        map(handle_testcases, testcases)

    def test_get_references(self):
        """
            Hmm.
            This could be tricky to test, really.
            Maybe not; maybe just a bunch of cases.
        """

        testcases = [
            {
                #substitutions that are links.
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem |testing|_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem |testing|_",
                    u"",
                    u".. |testing| replace:: `testing`",
                    u".. _testing:",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #substitutions
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem |testing|",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem |testing|",
                    u"",
                    u".. |testing| replace:: testing",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links in an unknown filetype
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `testing`_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `testing`_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"something else",
                    u"",
                    u".. _testing: ",
                ]),
            },
            {
                #links
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `testing`_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `testing`_",
                    u"",
                    u".. _testing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #text with indented insert point:
                "text": u"\n".join([
                    u"lorem ipsum:",
                    u"",
                    u"    .. container:: date",
                    u"",
                    u"lorem `test: ing`_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum:",
                    u"",
                    u"    .. container:: date",
                    u"",
                    u"lorem `test: ing`_",
                    u"",
                    u".. _test\: ing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links with colons
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `test: ing`_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `test: ing`_",
                    u"",
                    u".. _test\: ing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links with cites on same line
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `test: ing`_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `test: ing`_",
                    u"",
                    u".. _test\: ing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links with cites on same line already referenced
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `testing`_",
                    u"",
                    u".. _testing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `testing`_",
                    u"",
                    u".. _testing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links with colons and cites on same line already referenced
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `test: ing`_",
                    u"",
                    u".. _test\: ing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem `false` `test: ing`_",
                    u"",
                    u".. _test\: ing: ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links inside code (shouldn't be referenced)
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links inside code block (shouldn't be referenced)
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u"this is a code block::",
                    u"",
                    u"    some |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u"this is a code block::",
                    u"",
                    u"    some |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u".. |sub| replace:: sub",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #links inside code block (shouldn't be referenced)
                #multiple blocks
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u"this is a code block::",
                    u"",
                    u"    some |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u"this is a code block too::",
                    u"",
                    u"    some more |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem ```testing`_``",
                    u"",
                    u"lorem ``this is `testing`_ code blocks `too```",
                    u"",
                    u"this is a code block::",
                    u"",
                    u"    some |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u"this is a code block too::",
                    u"",
                    u"    some more |test| code here `testing`_",
                    u"",
                    u"normal para iwth a |sub| for good luck.",
                    u"",
                    u".. |sub| replace:: sub",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #Footnotes
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [testing]_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [testing]_",
                    u"",
                    u".. [testing] ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #Symbolic Footnotes
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [*]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [*]_",
                    u"",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [*]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [*]_",
                    u"",
                    u".. [*] ",
                    u".. [*] ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                #Numeric Footnotes
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u".. [#] ",
                    u".. [#] ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u".. [#] ",
                    u".. [#] ",
                    u".. container:: date",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u":PostID: [",
                    u"",
                    u"something else",
                ]),
            },
            {
                # Numeric Footnotes in default document
                "text": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                ]),
                "expected": u"\n".join([
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u"lorem ipsum",
                    u"",
                    u"lorem [#]_",
                    u"",
                    u".. [#] ",
                    u".. [#] ",
                ]),
            },
        ]

        def handle_testcases(case):
            self.rr.sourcetext = case["text"]
            self.rr.determine_filetype()
            result = self.rr.get_references()
            if result != case["expected"]:
                import nose; nose.tools.set_trace()
            assert result == case["expected"]

        map(handle_testcases, testcases)

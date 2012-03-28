#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""

* Take the file as input.
* Figure out what kind of file it is (blog, morning pages, etc.)
* Get the various kinds of references.
* Put them in the appropriate place in the file.
* Print out the file.

"""
import codecs
import json
import os
import re
import sys
from functools import partial
from itertools import takewhile
from optparse import OptionParser

class RSTReferencer(object):

    config_files = ["rest_get_refs.json"]
    options = {}

    def __init__(self):
        pass

    def cli_main(self):
        self.setup_config()
        self.setup_cli_options()
        self.handle_cli_options()
        self.determine_filetype()
        self.newtext = self.get_references()
        self.write_output()

    def setup_config(self):
        self.config = {"filetypes": {}, "patterns": []}
        for f in self.config_files:
            fp = os.path.join(os.path.dirname(__file__), f)
            conf = json.loads(open(fp).read())
            self.config["filetypes"].update(conf.get("filetypes",{}))
            self.config["patterns"] += conf.get("patterns", [])

    def setup_cli_options(self):
        parser = OptionParser()
        parser.add_option(
            "-f",
            "--file",
            dest="sourcefile",
            help="read from SOURCEFILE",
            metavar="SOURCEFILE"
        )
        parser.add_option(
            "-d",
            "--destination",
            dest="destfile",
            help="write to DESTFILE",
            metavar="DESTFILE"
        )
        options, self.arguments = parser.parse_args()
        optdict = vars(options)
        #Eliminate the empty keys:
        optdict = dict([k, v] for k, v in optdict.iteritems() if v)
        #Turn multiple-value params into arrays:
        optdict = self.multiple_values(optdict)
        self.options.update(optdict)

    def handle_cli_options(self):
        if not self.options.get("sourcefile", None):
            #Take stdin:
            self.sourcetext = sys.stdin.read()
        else:
            #Take the contents of the specified file:
            self.sourcefile = self.options.get("sourcefile")
            #f = open(self.options.get("sourcefile"), 'r')
            f = codecs.open(
                self.options.get("sourcefile"),
                mode="r",
                encoding="utf-8"
            )
            self.sourcetext = f.read()
        #
        if not self.options.get("destfile", None):
            #Store setting to write to stdout later:
            self.destination = {
                "write_to_file": False,
            }
        else:
            #Store setting to write to file later:
            self.destination = {
                "write_to_file": True,
                "file": self.options.get("destfile")
            }

    def determine_filetype(self):
        """
           Checks for the markers in the config file.
        """
        self.filetype = None
        for ft in self.config["filetypes"]:
            try:
                if self.config["filetypes"][ft]["marker"] in self.sourcetext:
                    self.filetype = self.config["filetypes"][ft]
            except UnicodeDecodeError:
                self.sourcetext = self.sourcetext.decode("utf-8")
                if self.config["filetypes"][ft]["marker"] in self.sourcetext:
                    self.filetype = self.config["filetypes"][ft]


    def get_references(self):
        text = self.sourcetext
        referencelist, sublist = [], []
        #get the already-present references:
        ref_re = re.compile(r"^(?P<ref>\.\. [\[|]{1}[^\]|]*[|\]])",
                            re.MULTILINE)
        matchlist = [match.group("ref") for match in ref_re.finditer(text)]
        refl_re = re.compile(r"^(?P<refl>\.\. _.*(?<!\\):)", re.MULTILINE)
        refllist = [match.group("refl") for match in refl_re.finditer(text)]
        matchlist = matchlist + refllist
        patterns = self.config.get("patterns", [])

        def make_regex(patdict):
            #We have to special-case the expressions that have "false closers"
            #that will fool the pattern, e.g. in this line:
            #test `test` test `test`_
            #we only want to match the last `test`_.
            regex = None
            if "false_closer" in patdict:
                regex = r"""
                    (?P<preceding>.{1})?
                    (?P<prethree>.{3})?
                    (?P<element>
                        (?P<opener>\%s)
                        (?P<content>[^%s]+?)
                        (?P<closer>\%s)
                    )
                """ % (
                    patdict["opener"],
                    patdict["false_closer"],
                    patdict["closer"]
                )
            else:
                regex = r"""
                    (?P<preceding>.{1})?
                    (?P<prethree>.{3})?
                    (?P<element>
                        (?P<opener>\%s)
                        (?P<content>.+?)
                        (?P<closer>\%s)
                    )
                """ % (
                    patdict["opener"],
                    patdict["closer"]
                )
            if patdict.get("multiline", False):
                return re.compile(regex, re.VERBOSE | re.DOTALL)
                #return re.compile(regex, re.VERBOSE)
            else:
                return re.compile(regex, re.VERBOSE)

        def substitute_pattern(patdict, text):
            regex = make_regex(patdict)
            def should_process(matchgroupdict, num_matches):
                content = patdict["reference_start"].format(**matchgroupdict)
                if content in (".. [*]", ".. [#]"):
                    # Special-case footnotes
                    if num_matches > matchlist.count(content):
                        return True
                if content in matchlist:
                    return False
                return True
            num_matches = len(regex.findall(text))
            for match in regex.finditer(text):
                comment, mgd, mgs = False, match.groupdict(), match.groups()
                if ":" in mgd["content"]:
                    mgd["content"] = mgd["content"].replace(":", "\\:")
                if comment:
                    pass
                if not comment and patdict.has_key("reference"):
                    if should_process(mgd, num_matches):
                        matchlist.append(patdict["reference_start"].format(**mgd))
                        referencelist.append(patdict["reference"].format(**mgd))
                        if patdict.get("substitute", False):
                            two = patdict["substitute"].format(**mgd)
                        else:
                            two = mgd["element"]
                        sublist.append((mgd["element"], two))
                if not comment and not patdict.has_key(
                    "reference") and patdict.has_key("substitute"):
                    sublist.append((
                        mgd["element"],
                        patdict["substitute"](mgd)
                    ))

            for sub in sublist:
                text = text.replace(sub[0], sub[1])
            return text

        """
        need to divide the text into sections, stripping out code snippets and
        code blocks, and then passing it to the pattern for loop.
        """

        lines = text.split(u"\n")
        def start_code_block(line):
            comment_or_directive_re = re.compile(r"\s*\.\. ")
            if comment_or_directive_re.match(line):
                return False

            eol_colons_re = re.compile(r"\s*::")
            if eol_colons_re.match(line[::-1]):
                return end_code_block

            return False

        def end_code_block(indent, line):
            if not line.strip():
                return False

            if not indent:
                nonspace_re = re.compile(r"^[^\s]{1}")
                if nonspace_re.match(line):
                    return ("CODE", 0)
            elif line.startswith(indent):
                return ("CODE", 0)

            return False


        def make_blocks(lns=[], curlines=[], blocks=[], endfn=None):
            if not lns:
                if curlines:
                    blocks.append(("TEXT", curlines))
                return blocks

            l = lns.pop(0)
            if endfn:
                if endfn(l):
                    if endfn(l)[1] == 0:
                        lns.insert(0, l)
                    else:
                        curlines.append(l)
                    blocks.append((endfn(l)[0], curlines))
                    curlines = []
                    endfn = None
                else:
                    #Have to assume that if it doesn't end a section, it just gets
                    #added to the section.
                    curlines.append(l)

                return make_blocks(lns=lns, curlines=curlines, blocks=blocks,
                                   endfn=endfn)

            if l.startswith(".. "):
                if curlines:
                    blocks.append(("TEXT", curlines))
                    curlines = []
                blocks.append(("COMMENTORDIRECTIVE", [l]))
                return make_blocks(lns=lns, curlines=curlines, blocks=blocks,
                                   endfn=endfn)

            if start_code_block(l):
                curlines.append(l)
                blocks.append(("TEXT", curlines))
                curlines = []
                indent_re = re.compile(r"^(?P<indent>\s*)")
                indent = indent_re.search(l).group()
                endfn = partial(end_code_block, indent)
                return make_blocks(lns=lns, curlines=curlines, blocks=blocks,
                                   endfn=endfn)

            curlines.append(l)
            return make_blocks(lns=lns, curlines=curlines, blocks=blocks,
                               endfn=endfn)


        #so the problem here is that we want to add \n to each block's text
        #lines except for the last block's last line.
        def join_block_text(block):
            blockt = "%s%s" % (u"\n".join(block[1]), u"\n")
            return (block[0], blockt)
        blocks = [join_block_text(b) for b in make_blocks(lns=lines)]
        blocks[-1] = (blocks[-1][0], blocks[-1][1][:-1])

        def process_block(textblock):
            if textblock[0] != "TEXT":
                return textblock[1]

            block = textblock[1]
            code_re = re.compile(r"(?P<code>``.*``)", re.VERBOSE)
            matches = [m for m in code_re.finditer(block)]
            chunks = []
            if matches:
                last_end = 0
                for m in matches:
                    chunks.append(("TEXT", block[last_end:m.start()]))
                    chunks.append(("CODE", m.group()))
                    last_end = m.end()
                chunks.append(("TEXT", block[last_end:]))
            else:
                chunks = [("TEXT", block)]

            def change_refs(chunk):
                operable_block = chunk[1]
                if chunk[0] == "TEXT":
                    for pattern in patterns:
                        operable_block = substitute_pattern(pattern, operable_block)
                return operable_block

            return u"".join([change_refs(c) for c in chunks])

        text = u"".join([process_block(b) for b in blocks])

        lines = text.split('\n')
        #Find the insertion point:
        if not self.filetype:
            prelines, postlines = lines + [u""], []
        else:
            def not_insert(l): return not l.startswith(self.filetype["insert"])
            prelines = list(takewhile(not_insert, lines))
            postlines = lines[len(prelines):]
        return u"\n".join(prelines + referencelist + postlines)

    def write_output(self):
        try:
            sys.setdefaultencoding("utf-8")
        except:
            pass
        os.environ["__CF_USER_TEXT_ENCODING"] = "0x1F5:0x8000100:0x8000100"
        if self.destination.get("write_to_file", False) and self.destination.get("file", False):
            #f = open(self.destination["file"], "w")
            f = codecs.open(
                self.destination["file"],
                mode="w",
                encoding="utf-8"
            )
            f.write(self.newtext)
            f.close()
        else:
            try:
                print self.newtext
            except UnicodeEncodeError:
                print self.newtext.encode("utf-8")
            #print sys.getdefaultencoding()

    def multiple_values(self, optdict):
        for key in ("scripts", "stylesheets"):
            val = optdict.get(key, None)
            optdict.update({key: val.split(",")} if val else {})
        return optdict

if __name__ == '__main__':
    referencer = RSTReferencer()
    referencer.cli_main()

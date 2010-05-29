import glob
import os.path
import datetime
from StringIO import StringIO
import textwrap
import re

class Repo(object):
    def __init__(self, wikiDir):
        self.wikiDir = wikiDir

    def list_documents(self):
        'get list of posts and pages from server, return as dictionary'
        d = {}
        for path in glob.glob(self.wikiDir + '/data/pages/*'):
            d[os.path.basename(path)] = {} # no metadata
        return d

    def get_document_history(self, doc_id):
        'get dictionary of revisions of this doc, each with dict containing timestamp'
        d = {}
        for path in glob.glob(self.wikiDir + '/data/pages/%s/revisions/0*' % doc_id):
            revID = os.path.basename(path)
            d[revID] = dict(timestamp=datetime.datetime.fromtimestamp(os.stat(path)
                                                                      .st_mtime))
        return d

    def get_document(self, doc_id, revID=None):
        'retrieve the specified post or page and convert to ReST'
        if revID is None:
            ifile = open(os.path.join(self.wikiDir, 'data', 'pages', doc_id, current))
            try:
                revID = ifile.read().strip()
            finally:
                ifile.close()
        ifile = open(os.path.join(self.wikiDir, 'data', 'pages', doc_id, 'revisions',
                                  revID))
        try:
            rest = StringIO()
            convert_moin_to_rest(ifile, rest)
        finally:
            ifile.close()
        return rest.getvalue(), {} # no metadata



def re_replace(pattern, formatter, line):
    hits = [m for m in pattern.finditer(line)]
    if len(hits) == 0:
        return line
    # replace all cases of the pattern
    newline = ''
    lastpos = 0
    for m in hits:
        rep = formatter(m.group(0))
        newline += line[lastpos:m.start()] + rep
        lastpos = m.end()
    newline += line[lastpos:]
    return newline

def rest_url(s):
    'reformat moin link to restructured text link'
    t = s[2:-2].split('|')
    if len(t) == 1:
        return '`<%s>`_' % t[0]
    url,text = t
    return '`%s <%s>`_' % (text, url)

anonymousLinks = []

def rest_internal_link(s):
    'format text for an internal link'
    link,text = s[2:-2].split('|')
    #anonymousLinks.append(link)
    return ':doc:`%s <%s>`' % (text,link)

moinReformatters = [
    (re.compile(r"\$\$.+?\$\$"), lambda s: ":math:`%s`" % s[2:-2]),
    (re.compile(r"'''''.+?'''''"), lambda s: "**%s**" %s[5:-5]),
    (re.compile(r"'''.+?'''"), lambda s: "**%s**" %s[3:-3]),
    (re.compile(r"''.+?''"), lambda s: "*%s*" %s[2:-2]),
    (re.compile(r"{{{.+?}}}"), lambda s: "``%s``" %s[3:-3]),
    (re.compile(r"\[\[[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+\|.+?\]\]"),
     rest_internal_link),
    (re.compile(r"\[\[[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+\]\]"),
     lambda s: ':doc:`%s`' % s[2:-2]),
    (re.compile(r"\[\[.+?\]]"), rest_url),
    (re.compile(r"\b[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+[^>A-Za-z0-9]"),
     lambda s: ' :doc:`%s`%s' % (s[:-1],s[-1])),
]

def reformat_line(line):
    for pattern,rep in moinReformatters: # apply inline substitutions
        line = re_replace(pattern, rep, line)
    return line

def convert_moin_to_rest(moinFile, outfile):
    'converts moin markup to restructured text, but very minimal'
    headers = ('=', '#', '-', '_', '^', '+', '.')
    indentList = [1]
    firstLevel = None
    it = iter(moinFile)
    for line in it:
        n = len(line)
        lineStripped = line.lstrip()
        try:
            firstChar = lineStripped[0]
        except IndexError:
            firstChar = ' '
        firstIndent = n - len(lineStripped)
        if line.startswith('='): # reformat section heading
            level = len(line.split()[0]) - 1
            if firstLevel is None:
                firstLevel = level
            elif level < firstLevel:
                level = firstLevel # don't create bad title
            line = line.strip().strip(' =\n')
            if level == 0: # top level title
                print >>outfile, headers[level] * len(line)
            print >>outfile, line
            print >>outfile, headers[level] * len(line)
            print >>outfile
        elif firstChar in '*123456789': # item list
            if firstChar != '*':
                firstChar = '#.'
            elif firstIndent > 0: # adjust for extra space added before *
                firstIndent -= 1
            line = line.lstrip(' *0123456789.') # find beginning of text
            line = reformat_line(line)
            newline = textwrap.fill(firstChar + ' ' + line.strip(),
                                    initial_indent=' ' * firstIndent,
                    subsequent_indent=' ' * (firstIndent + len(firstChar) + 1))
            print >>outfile, '\n' + newline            
        else:
            codePos = line.find('{{{')
            if codePos >= 0:
                codeLine = line[codePos+3:]
                line = line[:codePos] + '::'
            n = len(line)
            line = line.lstrip()
            nspace = n - len(line)
            line = reformat_line(line)
            newline = textwrap.fill(line.strip(),
                                    initial_indent=' ' * nspace,
                                    subsequent_indent=' ' * nspace)
            print >>outfile, '\n' + newline
            if codePos >= 0:
                outfile.write(codeLine)
                for line in it:
                    codePos = line.find('}}}')
                    if codePos >= 0:
                        print >>outfile, (' ' * (nspace + 2)) + line[:codePos]
                        break
                    outfile.write((' ' * (nspace + 2)) + line)
        if len(anonymousLinks) > 0:
            print >>outfile
        for link in anonymousLinks: # insert link to internal target 
            print >>outfile, '__ ' + link + '_'
        del anonymousLinks[:] # empty the list
            


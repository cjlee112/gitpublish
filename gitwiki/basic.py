
import os, glob, shutil, subprocess, time, re, textwrap, optparse, sys
try:
    import opml
except ImportError:
    pass


def write_opml_to_rest(opmlList, restFile, level=0):
    'recursive reST writer processes one layer of OPML'
    for o in opmlList:
        try:
            s = '* *' + o.text + '*'
        except AttributeError:
            s = '* '
        try:
            s += ': ' + o.Comment
        except AttributeError:
            pass
        output = textwrap.fill(s, initial_indent = ' ' * level,
                               subsequent_indent = '  ' + (' ' * level))
        print >> restFile, output + '\n'
        if len(o) > 0:
            write_opml_to_rest(o, restFile, level + 1)

def convert_opml_to_rest(opmlPath, restFile):
    'write reST for an OPML outline'
    opmlData = opml.parse(opmlPath)
    print >>restFile, '=' * len(opmlData.title)
    print >>restFile, opmlData.title
    print >>restFile, ('=' * len(opmlData.title)) + '\n'
    write_opml_to_rest(opmlData, restFile)

def convert_opml_files(opmlfiles):
    for filename in opmlfiles:
        if filename.endswith('.opml'):
            restFilename = filename[:-4] + 'rst'
        else:
            restFilename = filename + '.rst'
        outfile = file(restFilename, 'w')
        try:
            convert_opml_to_rest(filename, outfile)
        finally:
            outfile.close()
            

def simpletext_to_rest(textFile, restFile, headerMark=':', headerMax=40):
    """Trivial reformatter suitable for text copied from a word
processing document, i.e. it applies text-wrapping to produce
a basic reST format.  It follows a few simple rules:

* lines starting with '*' are treated as list items.

* lines that contain a colon (or any headerMark you specify)
  are treated as section headers.

* the first section header is treated as the Document Title, up to
  the colon (or headerMark).

* other lines are treated as paragraphs, and are line-wrapped, with
  an extra blank line inserted between paragraphs.
  """
    firstHeader = True
    for line in textFile:
        line = line.strip()
        nchar = line.find(headerMark)
        if line.startswith('*'): # treat as list item
            print >>restFile, textwrap.fill(line, subsequent_indent='  ') \
                  + '\n'
        elif nchar < headerMax and nchar > 0 : # treat as title
            if firstHeader:
                firstHeader = False
                title = line[:nchar]
                print >>restFile, '=' * len(title)
                print >>restFile, title
                print >>restFile, '=' * len(title)
                subtitle = line[nchar + len(headerMark):]
                print >>restFile, '\n*' + subtitle.strip() + '*\n'
            else: # treat as section heading
                if line.endswith(headerMark): # remove terminal headerMark
                    line = line[:-len(headerMark)]
                print >>restFile, line + '\n' + ('-' * len(line)) + '\n'
        else: # treat as regular paragraph: apply textwrap
            print >>restFile, textwrap.fill(line) + '\n'

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
            

def convert_file(pageRev, destDir):
    t = os.path.split(pageRev)
    version = int(t[1])
    filename = os.path.basename(os.path.dirname(t[0]))
    destFile = os.path.join(destDir, filename + '.rst')
    ifile = file(pageRev)
    try:
        ofile = file(destFile, 'w')
        try:
            ofile.write('.. _%s:\n\n' % filename) # target for internal link
            convert_moin_to_rest(ifile, ofile)
        finally:
            ofile.close()
    finally:
        ifile.close()
    return destFile, filename, version

def commit_moin_revision(pageRev, destDir):
    'commit a specified revision to git repository in destDir'
    destFile, filename, version = convert_file(pageRev, destDir)
    cmd = ['git', 'add', destFile]
    subprocess.call(cmd)
    revTime = time.ctime(os.stat(pageRev).st_mtime)
    commitMsg = '%s revision %d, %s' %(filename, version, revTime)
    cmd = ['git', 'commit', '-m', commitMsg]
    subprocess.call(cmd)
            
def commit_moin_by_time(wikiDir, destDir, filterfunc=None):
    'commit all revisions in wikiDir to git repo in destDir'
    revFiles = glob.glob(wikiDir + '/*/revisions/0*')
    if filterfunc:
        revFiles = filter(filterfunc, revFiles)
    l = [(os.stat(f).st_mtime,f) for f in revFiles]
    l.sort()
    for t in l:
        commit_moin_revision(t[1], destDir)

def copy_moin_current(wikiDir, destDir, filterfunc=None):
    'copy the latest versions of all pages in wikiDir to destDir'
    revFiles = glob.glob(wikiDir + '/*/current')
    if filterfunc:
        revFiles = filter(filterfunc, revFiles)
    for pageCurrent in revFiles:
        ifile = file(pageCurrent)
        try:
            line = ifile.read().strip()
        finally:
            ifile.close()
        pageRev = os.path.join(os.path.dirname(pageCurrent), 'revisions', line)
        convert_file(pageRev, destDir)


def option_parser():
    parser = optparse.OptionParser()

    parser.add_option(
        '--simpletext', action="store", type='string',
        dest="simpletext", 
        help="simpletext file to convert"
    )

    parser.add_option(
        '--opmlfiles', action="store_true", dest="opmlfiles",
        default=False, 
        help="runs the performance tests (not implemented)"
    )

    return parser

if __name__ == '__main__':
    parser = option_parser()
    options, args = parser.parse_args()
    if options.simpletext:
        textFile = file(options.simpletext)
        try:
            simpletext_to_rest(textFile, sys.stdout)
        finally:
            textFile.close()
    elif options.opmlfiles:
        convert_opml_files(args)

            

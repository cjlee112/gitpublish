
import os, glob, shutil, subprocess, time, re, textwrap


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
    return ':ref:`%s <%s>`' % (text,link)

moinReformatters = [
    (re.compile(r"\$\$.+?\$\$"), lambda s: ":math:`%s`" % s[2:-2]),
    (re.compile(r"'''''.+?'''''"), lambda s: "**%s**" %s[5:-5]),
    (re.compile(r"'''.+?'''"), lambda s: "**%s**" %s[3:-3]),
    (re.compile(r"''.+?''"), lambda s: "*%s*" %s[2:-2]),
    (re.compile(r"{{{.+?}}}"), lambda s: "``%s``" %s[3:-3]),
    (re.compile(r"\[\[[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+\|.+?\]\]"),
     rest_internal_link),
    (re.compile(r"\[\[[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+\]\]"),
     lambda s: ':ref:`%s`' % s[2:-2]),
    (re.compile(r"\[\[.+?\]]"), rest_url),
    (re.compile(r"\b[A-Z]+[a-z0-9]+[A-Z][A-Za-z0-9]+\b"),
     lambda s: ':ref:`%s`' % s),
]

def convert_moin_to_rest(moinFile, outfile):
    'converts moin markup to restructured text, but very minimal'
    headers = ('=', '#', '-', '_', '^', '+', '.')
    indentList = [1]
    firstLevel = None
    it = iter(moinFile)
    for line in it:
        for pattern,rep in moinReformatters: # apply inline substitutions
            line = re_replace(pattern, rep, line)
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
        elif line.strip().startswith('*'): # item list
            indent = line.find('*')
            if indent > indentList[-1]:
                indentList.append(indent)
            else:
                while len(indentList)>1 and indent < indentList[-1]:
                    indentList.pop()
            nspace = 2 * len(indentList)
            newline = textwrap.fill(line.strip(),
                                    initial_indent=' ' * (nspace - 2),
                                    subsequent_indent=' ' * nspace)
            print >>outfile, '\n' + newline            
        else:
            codePos = line.find('{{{')
            if codePos >= 0:
                codeLine = line[codePos+3:]
                line = line[:codePos] + '::'
            n = len(line)
            line = line.lstrip()
            nspace = n - len(line)
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
            
            

def commit_moin_revision(pageRev, destDir):
    'commit a specified revision to git repository in destDir'
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
        

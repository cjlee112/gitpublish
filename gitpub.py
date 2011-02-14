#!/usr/bin/env python

import optparse
from gitpublish import core
try:
    import getpass
except ImportError:
    pass

class Interface(object):
    '''provides a command line interface designed to be invoked separately
    for each action (rather than working with Python objects in Python interpreter).'''
    def __init__(self):
        self.localRepo = core.GitRepo()

    def on_remote_branch(self):
        '''get current remote name and branch name if on tracking branch,
        or raise ValueError'''
        branchName = self.localRepo.branch()
        if branchName.startswith('gpremotes/'):
            return branchName.split('/')[1:]
        else:
            raise ValueError('not on a gitpublish remote branch!')

    def get_tracking_branch(self, remoteName=None, branchName='master',
                            doCheckout = True):
        'get specified tracking branch, or current tracking branch'
        if remoteName is None:
            remoteName, branchName = self.on_remote_branch()
            doCheckout = False
        return core.TrackingBranch(remoteName, self.localRepo, branchName,
                                   doFetch=False, doCheckout=doCheckout)

    def remote_list(self):
        'get a list of gpremotes'
        branches = [s for s in self.localRepo.list_branches() if
                    s.startswith('gpremotes/')]
        remotes = set()
        for branch in branches:
            remotes.add(branch.split('/')[1])
        return tuple(remotes)

    def remote_add(self, remoteName, remotePath, branchName=None,
                   doFetch=False):
        'add a new gpremote'
        if branchName: # switch to specified branch for adding this remote
            self.localRepo.branch(branchName)
        else: # use current branch name
            branchName = self.localRepo.branch()
        l = remotePath.split(':') # parse type:path:arg1:arg2... format
        remoteType = l[0]
        s = l[1]
        i = s.find('@') # parse user@host format
        if i < 0:
            host = s
            user = getpass.getuser() # default username
        else:
            host = s[i + 1:]
            user = s[:i]
        repoArgs = dict(host=host, user=user)
        for arg in l[2:]: # extract optional key=value arguments
            i = arg.index('=')
            repoArgs[arg[:i]] = arg[i + 1:]
        tb = core.TrackingBranch(remoteName, self.localRepo, branchName,
                                 doFetch=doFetch, autoCreate=True,
                                 remoteType=remoteType, repoArgs=repoArgs)

    def checkout(self, remotename, branchName='master'):
        'checkout specified tracking branch'
        self.localRepo.checkout('/'.join(('gpremotes', remotename, branchName)))

    def add(self, paths, **docDict):
        'add file to mapping to be published on remote'
        tb = self.get_tracking_branch()
        for path in paths:
            tb.add(path, **docDict)
        tb.save_stage()

    def rm(self, paths):
        'remove file from mapping (to unpublish it on remote)'
        tb = self.get_tracking_branch()
        for path in paths:
            tb.rm(path)
        tb.save_stage()

    def mv(self, oldpaths, newpath):
        'move file locally, while continuing to publish it on remote'
        for oldpath in oldpaths:
            self.localRepo.mv(oldpath, newpath)

    def commit(self, message):
        'commit any mapping changes to *local* repository.  Does not push to remote!'
        self.on_remote_branch() # make sure we're on remote tracking branch
        self.localRepo.commit(message)

    def fetch(self, remoteName=None, branchName='master'):
        'fetch latest changes from remote, commit to tracking branch'
        tb = self.get_tracking_branch(remoteName, branchName)
        tb.fetch()

    def push(self, remoteName=None, branchName='master'):
        'push mapped documents from this tracking branch to publish on remote'
        tb = self.get_tracking_branch(remoteName, branchName)
        tb.push()

    def merge(self, branchName=None, updateOnly=False):
        'merge changes from this tracking branch'
        tb = self.get_tracking_branch()
        if not branchName:
            branchName = tb.branchName.split('/')[-1]
        tb.merge(branchName, updateOnly)


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        '-f', '--fetch', action="store_true", dest="doFetch", default=False,
        help='fetch updates when creating new remote')
    parser.add_option(
        '--update-only', action="store_true", dest="updateOnly", default=False,
        help='''Force gitpublish merge to only perform doc map updates,
i.e. skip its automatic merge step.  Only use this option if you
manually merged in changes from your local branch to your
gpremotes/ tracking branch, before running gitpublish merge.''')
    parser.add_option(
        '-m', action="store", type="string",
        dest="message", 
        help="message to store for this commit")
    parser.add_option(
        '--docarg', action='append', dest='docargs', default=[],
        help='''optional doc arguments for gitpub add:
        pubtype="post|page" ... for wordpress, sets the publication type''')
    return parser.parse_args()



if __name__ == '__main__':
    options, args = get_options()
    cmd = args[0]
    args = args[1:]
    gp = Interface()
    if cmd == 'remote':
        if len(args) == 0:
            for remote in gp.remote_list():
                print remote
        elif args[0] == 'add':
            gp.remote_add(doFetch=options.doFetch, *args[1:])
        else:
            raise ValueError('gitpub remote so far only supports the add command')
    elif cmd == 'checkout':
        gp.checkout(*args)
    elif cmd == 'add':
        docDict = {}
        for arg in options.docargs:
            i = arg.index('=')
            docDict[arg[:i]] = arg[i + 1:]
        gp.add(args, **docDict)
    elif cmd == 'rm':
        gp.rm(args)
    elif cmd == 'mv':
        gp.mv(args[:-1], args[-1])
    elif cmd == 'commit':
        gp.commit(options.message)
    elif cmd == 'fetch':
        gp.fetch(*args)
    elif cmd == 'push':
        gp.push(*args)
    elif cmd == 'merge':
        if len(args) > 1:
            raise ValueError('usage: gitpublish merge [local-branch-name]')
        gp.merge(updateOnly=options.updateOnly, *args)
    else:
        raise ValueError('not a valid command: remote, checkout, add, rm, mv, commit, fetch, push, merge')

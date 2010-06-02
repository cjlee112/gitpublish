import sys
import optparse
from gitpublish import core

def option_parser():
    parser = optparse.OptionParser()
    return parser

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

    def get_tracking_branch(self, remoteName=None, branchName='master'):
        'get specified tracking branch, or current tracking branch'
        if remoteName is None:
            remoteName, branchName = self.on_remote_branch()
            doCheckout = False
        else:
            doCheckout = True
        return core.TrackingBranch(remoteName, self.localRepo, branchName,
                                   doFetch=False, doCheckout=doCheckout)

    def checkout(self, remotename, branchName='master'):
        'checkout specified tracking branch'
        self.localRepo.checkout('/'.join(('gpremotes', remotename, branchName)))

    def add(self, path, **docDict):
        'add file to mapping to be published on remote'
        tb = self.get_tracking_branch()
        tb.add(path, **docDict)
        tb.save_stage()

    def rm(self, path, **docDict):
        'remove file from mapping (to unpublish it on remote)'
        tb = self.get_tracking_branch()
        tb.rm(path)
        tb.save_stage()

    def mv(self, oldpath, newpath):
        'move file locally, while continuing to publish it on remote'
        tb = self.get_tracking_branch()
        tb.mv(path)
        tb.save_stage()

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

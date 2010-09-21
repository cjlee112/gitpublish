
===============================================
Using Gitpublish to publish to a WordPress Blog
===============================================

Creating a Git branch to manage your WordPress blog
---------------------------------------------------

Let's assume I have a git repository in ``/Users/leec/test/gitpublish/test3``
that already has at least one commit in it (so it contains at least one
valid branch).  Let's create a "remote tracking branch" off of our current
branch (e.g. master) that will manage my WordPress blog.

Starting in my git repo directory, I fire up Python and create an
object representing this tracking branch::

  >>> from gitpublish import core
  >>> gitrepo = core.GitRepo('/Users/leec/test/gitpublish/test3')
  >>> tb = core.TrackingBranch('tab', gitrepo, autoCreate=True, 
                               remoteType='wordpress',
                               repoArgs=dict(host='thinking.bioinformatics.ucla.edu',
                                             user='leec', blog_id=3))
  Switched to branch 'gpremotes/tab/master'
  Enter password for leec on thinking.bioinformatics.ucla.edu:
  [gpremotes/tab/master 3a9d48d] fetch from remote
   22 files changed, 2645 insertions(+), 0 deletions(-)
   create mode 100644 .gitpub/tab.json
   create mode 100644 .gitpub/tab.lastpush.json
   create mode 100644 tab-import/page:17.rst
   ...

A few notes:

* I gave my remote repo the nickname ``tab`` (my blog is called
  *Thinking About Bioinformatics*).  Gitpublish by default
  will therefore name the tracking branch ``gpremotes/tab/master``.

* ``autoCreate=True`` makes it create the tracking branch if it
  doesn't already exist.

* the ``remoteType`` argument controls what plugin gitpublish
  will use to connect to the remote server, in this case
  the ``gitpublish/plugin/wordpress.py`` module.

* ``repoArgs`` gets passed to the ``wordpress.Repo`` constructor
  to tell it how to connect to your WordPress server via XMLRPC.

* Note that if you specify your blog password as an argument
  to the repoArgs (``password='yourpassword'``), it will get
  saved to the mapping file ``.gitpub/tab.json``, which gets
  commited as part of this git branch and therefore will be
  visible to anyone you share this git repo branch with.
  You probably don't want that.
  Instead, I simply omit ``password`` from the repoArgs, forcing
  gitpublish to ask me for my password the first time that
  it needs it.  This mimics how ``git`` normally connects to
  remote repositories via ssh.

* Since this branch did not already exist, gitpublish
  first fetches all the existing documents from the wordpress blog,
  and checks them into this branch, so that this branch is in
  sync with the remote wordpress blog's state.

* Note that most of the messages above come from ``git``, not gitpublish
  itself.

* FYI, the file ``.gitpub/tab.json`` stores the current mapping of
  your local repository files in this branch to documents on the remote
  "repository" (in this case my WordPress blog).  It's stored in
  JSON, an easily readable text format that has the added virtue
  of working well with Git.  That is, as individual file mappings
  change in this map, that will only change a few lines in this
  file, so Git's diff / merge tools will work well with them.

* FYI, the file ``tab.lastpush.json`` represents a snapshot of this
  mapping at the most recent push / fetch synch event.  In
  other words, this represents a snapshot of what is actually
  on the remote server (assuming you aren't fiddling with content on
  the remote server outside of gitpublish).

Adding new content to our blog via a gitpublish push
----------------------------------------------------

Next, let's add a restructured text file as a new blog entry with
an associated image file::

  >>> tb.add('/Users/leec/test/gitpublish/test3/index.rst')
  >>> tb.add('/Users/leec/test/gitpublish/test3/summer_tanager_3_B.jpg')
  >>> tb.commit('added files')
  A	index.rst
  A	summer_tanager_3_B.jpg
  [gpremotes/tab/master dd0a1fd] added files
   3 files changed, 29 insertions(+), 0 deletions(-)
   create mode 100644 index.rst
   create mode 100644 summer_tanager_3_B.jpg

This does several things:

* if these files were not already tracked as part of your git repo,
  they are added via ``git add``.

* They are "staged" for being pushed to the remote server, by 
  being added to your local-to-remote document mapping, with
  an annotation that they don't yet have a corresponding document
  on the remote repository.

* The ``commit`` saves this "staging information" to your git branch
  ``gpremotes/tab/master`` so you can use all the power of ``git`` to
  manage this information in the future.

Finally we push our branch to the wordpress blog::

  >>> tb.push()
  [gpremotes/tab/master 678a10f] publish doc changes to remote
   2 files changed, 48 insertions(+), 2 deletions(-)

FYI, the two files that changed were of course just the mapping
files ``.gitpub/tab.json`` and ``.gitpub/tab.lastpush.json``.  Note
that this implies that a ``push`` event always creates a commit
(which records the change in mappings on the remote "repository").

Working with an existing Gitpublish branch
------------------------------------------

Say I come back to my git repository in the future, after having
made changes to ``index.rst`` on the ``master`` branch.  I want
to use Gitpublish to push these changes automatically to my 
WordPress blog.  Within my repository directory,
I start a new Python session::

   >>> from gitpublish import core
   >>> tb = core.TrackingBranch('tab', doFetch=False)
   >>> tb.push()
   [gpremotes/tab/master 1c22589] updated gpremotes/tab/master docmap from master
    1 files changed, 1 insertions(+), 1 deletions(-)
   Enter password for leec on thinking.bioinformatics.ucla.edu:
   [gpremotes/tab/master 59991bc] publish doc changes to remote
    2 files changed, 3 insertions(+), 3 deletions(-)

A few notes:

* If the git repo already contains a Gitpublish remote branch,
  all you have to give to :class:`core.TrackingBranch` is its
  name (in this case, ``tab``).

* Since we didn't specify a git repository, it assumes
  you are somewhere inside a git repository, and searches upwards
  from the current directory until it finds the top of the git
  repository (i.e. a directory containing a ``.git`` directory).

* The ``doFetch=False`` argument tells it that there is no need
  to check the remote repository for updates at this time.

* ``tb.push()`` does the equivalent of 
  ``git push <remotename> <branchname>``: it pushes
  the contents of the specified branch (which defaults to ``master``)
  to the remote branch represented by the ``tb`` object.

* This involves two steps: first it *merges* in changes from
  the ``master`` branch into this tracking branch (as shown
  by the first commit message above); second it transmits
  the changed content to the remote, and updates its mapping files
  to reflect those updates (as shown by the second commit message
  above).


  

===============================================
Using Gitpublish to publish to a WordPress Blog
===============================================

Creating a Git branch to manage your WordPress blog
---------------------------------------------------

Let's assume I have a git repository in ``/Users/leec/test/gitpublish/test3``
that already has at least one commit in it (so it contains at least one
valid branch).  Let's create a "remote tracking branch" off of our current
branch (e.g. master) that will manage my WordPress blog.

Starting in my git repo directory, I create a new remote tracking
branch::

  $ gitpub.py remote add ie wordpress:cjlee112@infoevolution.wordpress.com
  Switched to branch 'gpremotes/ie/master'
  [gpremotes/ie/master 70313f9] create new tracking branch
   2 files changed, 18 insertions(+), 0 deletions(-)
   create mode 100644 .gitpub/ie.json
   create mode 100644 .gitpub/ie.lastpush.json

A few notes:

* I gave my remote repo the nickname ``ie`` (my blog is called
  *Information Evolution*).  Gitpublish by default
  will therefore name the tracking branch ``gpremotes/ie/master``.

* the "remote URL" consists of a *remoteType* (wordpress),
  an optional *user name* (cjlee112; if not specified, it uses
  your current user name), and a *host* (infoevolution.wordpress.com).

* the ``remoteType`` argument controls what plugin gitpublish
  will use to connect to the remote server, in this case
  the ``gitpublish/plugin/wordpress.py`` module.

* By default, gitpublish does *not* fetch all documents from the
  remote.  You can force it to do so by passing the ``--fetch``
  option.  It would then
  fetch all the existing documents from the wordpress blog,
  and check them into this branch, so that this branch is in
  sync with the remote wordpress blog's state.  This would
  make sense if you wanted to use this repo as a "local mirror"
  in which you can manage all the documents in your blog.

* The default (no fetch) behavior is preferable if you just
  want to push individual documents from this repo to your
  blog.  Note that you could use this behavior to push
  different documents from several different local repositories
  to the same blog.

* Note also that you are perfectly free to create and edit
  *other* documents (i.e. documents not pushed by gitpublish)
  directly on your blog.  This will not cause any problems
  for gitpublish.  Of course, if you use a non-gitpublish
  interface to edit, those changes will not be tracked in your
  local git / gitpublish repository.

* FYI, the file ``.gitpub/ie.json`` stores the current mapping of
  your local repository files in this branch to documents on the remote
  "repository" (in this case my WordPress blog).  It's stored in
  JSON, an easily readable text format that has the added virtue
  of working well with Git.  That is, as individual file mappings
  change in this map, that will only change a few lines in this
  file, so Git's diff / merge tools will work well with them.

* FYI, the file ``ie.lastpush.json`` represents a snapshot of this
  mapping at the most recent push / fetch synch event.  In
  other words, this represents a snapshot of what it last pushed
  to the remote server.

* Note that most of the messages above come from ``git``, not gitpublish
  itself.

Adding new content to our blog via a gitpublish push
----------------------------------------------------

Next, let's add a restructured text file as a new blog entry with
an associated image file::

  $ gitpub.py add index.rst summer_tanager_3_B.jpg
  $ gitpub.py commit -m 'added two files'
  [gpremotes/ie/master e9b7503] add two files
   1 files changed, 8 insertions(+), 1 deletions(-)

This does several things:

* The two files are "staged" for being pushed to the remote server, by 
  being added to your local-to-remote document mapping, with
  an annotation that they don't yet have a corresponding document
  on the remote repository.

* The ``commit`` saves this "staging information" to your git branch
  ``gpremotes/ie/master`` so you can use all the power of ``git`` to
  manage this information in the future.  Specifically, they are
  registered in the ``.gitpub/ie.json`` file mentioned above.

Finally we push our branch to the wordpress blog::

  $ gitpub.py push
  Already up-to-date.
  [gpremotes/ie/master 2cf39fc] updated gpremotes/ie/master docmap from master
   1 files changed, 2 insertions(+), 0 deletions(-)
  Enter password for cjlee112 on infoevolution.wordpress.com:
  [gpremotes/ie/master e41d69e] publish doc changes to remote ie
   2 files changed, 52 insertions(+), 5 deletions(-)

* The initial "Already up-to-date" message simply means that 
  all changes on your tracking branch are merged 

* Note that when gitpublish pushes to the remote server, it
  has to update its local mapping files to record information
  about the "remote path" where each pushed document is
  stored on the remote.  In the case of WordPress, that basically
  consists of the post ID (or page ID) that WordPress assigns
  to each document.

* Note that gitpublish asks you to enter your password 
  whenever it needs to access the remote server.  Gitpublish
  does not store your password in any local file, for obvious
  security reasons.

* FYI, the two local files that changed were of course just the mapping
  files ``.gitpub/ie.json`` and ``.gitpub/ie.lastpush.json``.

Pushing local updates to a remote server
----------------------------------------

Say I come back to my git repository in the future, after having
made changes to ``index.rst`` on the ``master`` branch.  I want
to use Gitpublish to push these changes automatically to my 
WordPress blog.  Within my repository directory,
I checkout my gitpublish tracking branch, merge and push the
latest changes::

   $ gitpub.py checkout ie
   Switched to branch 'gpremotes/ie/master'
   $ gitpub.py merge
   Merge made by recursive.
    index.rst          |    2 +-
    2 files changed, 6 insertions(+), 1 deletions(-)
   [gpremotes/ie/master ebbede7] updated gpremotes/ie/master docmap from master
    1 files changed, 5 insertions(+), 5 deletions(-)
   $ gitpub.py push
   Already up-to-date.
   Enter password for cjlee112 on infoevolution.wordpress.com:
   [gpremotes/ie/master 974a224] publish doc changes to remote ie
    2 files changed, 15 insertions(+), 15 deletions(-)

A few notes:

* if you're on a local branch (e.g. ``master``) associated with a 
  gitpublish remote tracking branch (e.g. ``gpremotes/ie/master``),
  you only need to give the name of the remote; it will checkout
  the tracking branch associated with your current branch.

* Similarly, the ``merge`` command by default will merge changes
  from the local branch associated with the current gpremotes
  tracking branch (i.e. in this case, from ``master``).

Renaming local files published with Gitpublish
----------------------------------------------

If you want to rename a local file that you've already published
to a remote using Gitpublish, you need to tell Gitpublish where
you're moving it to.  You just use the standard ``git mv`` syntax::

   $ git checkout master
   $ gitpub.py mv index.rst mypost.rst
   $ git commit -m 'renamed index.rst'
   [master 98e0f36] renamed index.rst
    2 files changed, 5 insertions(+), 0 deletions(-)
    create mode 100644 .gitpub/_git_moves.json
    rename index.rst => mypost.rst (100%)

* Instead of saying ``git mv ...`` you just type ``gitpub.py mv ...``.
  This allows Gitpublish to record the necessary information about
  where you moved the file to, so it can "do the right thing" in
  future Gitpublish merge operations (i.e. it will need to propagate
  the filename change to its document maps).

* Note that you do this ``mv`` operation on your **local** branch, as usual.

* Note that Gitpublish mv adds an extra file to the commit:
  ``.gitpub/_git_moves.json``, which records the move operation(s)
  you performed.

We can now continue making modifications to our new file name::

   $ git add mypost.rst
   $ git commit -m 'minor change'
   [master e7e31f1] minor change
    1 files changed, 1 insertions(+), 1 deletions(-)

The next time you run Gitpublish merge in your remote tracking branch,
all these changes will be propagated automatically::

   $ gitpub.py checkout ie
   Switched to branch 'gpremotes/ie/master'
   $ gitpub.py merge
   Merge made by recursive.
    .gitpub/_git_moves.json |    5 +++++
    index.rst => mypost.rst |    2 +-
    2 files changed, 6 insertions(+), 1 deletions(-)
    create mode 100644 .gitpub/_git_moves.json
    rename index.rst => mypost.rst (79%)
   [gpremotes/ie/master b39ef75] updated _git_moves_merged.json
    1 files changed, 5 insertions(+), 0 deletions(-)
    create mode 100644 .gitpub/_git_moves_merged.json
   [gpremotes/ie/master 80a19b8] updated gpremotes/ie/master docmap from master
    1 files changed, 5 insertions(+), 5 deletions(-)

And we can then just push as usual::

   $ gitpub.py push
   Already up-to-date.
   Enter password for cjlee112 on infoevolution.wordpress.com:
   [gpremotes/ie/master d6ca583] publish doc changes to remote ie
    2 files changed, 15 insertions(+), 15 deletions(-)


  
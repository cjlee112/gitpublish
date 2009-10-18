
==================
The Gitwiki Design
==================

A Git-like Interface for Publishing
-----------------------------------

Git provides a clean model for "pulling" work from other people
and places, and "pushing" to other repositories to publish your
work.  I would like to use this same basic interface, for extracting
text from other sources (e.g. MS Word, wikis like MoinMoin etc.)
and for publishing content to external channels like WordPress.
This would allow us to manage and edit our content under git
with its powerful branch, merge and history tools, while publishing
content to the world via best-of-breed tools like WordPress.  
Many publishing tools try to provide a "complete solution",
but are only mediocre at each specific function.  I
want the freedom to use the best tool for each distinct function:
git for version control; WordPress for publishing; Restructured
Text (and all its associated tools like docutils and Sphinx)
for cross-compiling my content to any desired target format.

Instead of expounding on Git's many wonderful capabilities, I
want to zero in on one specific feature: git *remotes*::

   git remote add upstream git://github.com/cjlee112/pygr.git

creates a new *remote* called ``upstream``, which points to a
git repository at github.com.  We can then immediately fetch
all the latest updates from that repository using::

   git fetch upstream

They show up as *remote-tracking branches* in your local repository
with names like ``remotes/upstream/master`` (which tracks the 
``master`` branch in the ``upstream`` repository).  We can view
all the commits on those branches, using tools like ``gitk``
and see exactly what was added or changed.  We can merge
content from a given remote branch into our current branch
as easily as::

   git merge remotes/upstream/master

and I can push content from my master branch to ``upstream`` by typing::

   git push upstream master

I want to do exactly the same thing with remote "containers"
that are *not* git repositories.  For example::

   gitwiki remote add my_wordpress wordpress:thinking.bioinformatics.ucla.edu


creates a new *remote* called ``my_wordpress``, which points to a
WordPress website at ``thinking.bioinformatics.ucla.edu``.  I can 
then push restructured text content from my master branch
to that WordPress blog as simply as::

   gitwiki push my_wordpress master

Of course, this requires some transparent magic to automatically
convert the restructured text to the style of HTML that WordPress uses,
and upload the content via XMLRPC.  Gitwiki is all about automating 
such standard conversion and transmission tasks, and integrating
them in a clean way with the power of git.


The Gitwiki Interface
---------------------

* *add a remote*::

    gitwiki remote add <remotename> <protocol>:<address>

* *fetch* updates from a remote as (new) git branches and commits::

    gitwiki fetch <remotename>

  New commits show up on branches named
  ``gwremotes/<remotename>/<branchname>``.  New files will be automatically
  converted to the local format(s) specified by your gitwiki
  config file (i.e. ``.rst``, ``.csv``, ``.opml`` etc.).

* *add* a local file to be published on a particular remote::

    gitwiki add -r my_wordpress bigdoc.rst

Note that just like ``git add``, this simply *marks* the file
for addition to the remote.  This change won't actually be pushed
to the remote until you tell it to (see below).

* *remove* a local file from publication on a particular remote::

    gitwiki rm -r my_wordpress bigdoc.rst

* *push* my changes to the remote (to publish them)::

    gitwiki push my_wordpress master





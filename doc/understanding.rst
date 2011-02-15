
========================
Understanding Gitpublish
========================

* Gitpublish just works on top of Git.  It works on any Git repository.

* You manage your repository using Git as usual.

* Gitpublish gives you a few extra commands (for publishing content
  to remote servers), whose syntax mirrors Git commands that you
  already know.

* Under the hood, all Gitpublish is doing is creating Git
  branches (named ``gpremotes/REMOTENAME/BRANCHNAME``) in which
  it tracks what you publish to different remote servers.

For usage examples, see :doc:`tutorials/intro`.

The Gitpublish Command List
---------------------------

The Gitpublish command line interface simply mirrors the ``git``
interface.  You use Gitpublish by simply typing ``gitpub.py COMMAND [OPTIONS]``
instead of ``git COMMAND [OPTIONS]``.  However, this only applies
to a subset of git commands that Gitpublish needs to "intercept"
in order to work its magic:

* **gitpub.py remote**: if you want to list the Gitpublish remote servers you've
  previously created, or add a new one.

* **gitpub.py checkout**: if you want to checkout a Gitpublish remote
  tracking branch

* **gitpub.py add**: if you want to designate a local repository file for
  publication to the remote server.

* **gitpub.py rm**: if you want to *stop* publishing a local repository file
  to the remote server.

* **gitpub.py mv**: if you want to rename a local repository file that
  is already published to the remote server.

* **gitpub.py commit**: to commit any of the above changes to your
  remote tracking branch.

* **gitpub.py merge**: to merge changes from a local repository branch, to 
  the current remote tracking branch.

* **gitpub.py push**: to push changes from the current remote tracking branch,
  to the remote server.

* **gitpub.py fetch**: to fetch the latest content snapshot / changes from
  the remote server, to this remote tracking branch.

Note that apart from these specific usages, you should just use the
usual ``git COMMAND...`` syntax as usual for all other interactions with git.
For example:

* use **git remote** as usual to manage your git remotes.  Gitpublish's
  "remote tracking branches" are distinct from these.
  (Strictly speaking, Gitpublish's "remote tracking branches" are 
  just *local* git branches named ``gpremotes/REMOTENAME/BRANCHNAME``).

* use **git checkout** as usual to checkout branches. 
  (Strictly speaking, you can also use it to checkout Gitpublish
  tracking branches; ``gitpub.py checkout`` is only provided as
  a convenience -- it saves you from having to type the branch name).

* use **git add/rm/mv** to add, remove, or rename local files
  for commiting to git.

* use **git commit/merge/push/fetch** to commit changes to git,
  merge into local branches, push to or fetch from git remotes.


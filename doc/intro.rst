
==================================================================
Gitpublish: Using Git and Restructured Text as a Publishing System
==================================================================

Why use Git for publishing?
---------------------------

Distributed version control systems like Git solve one of the basic 
problems of collaborating on text projects 
-- how to let everyone have autonomy (i.e. edit their
version of some content as they like), while sharing with others.
Each user can have their own copy, edit it however they like,
but then make their changes available to others, who can pull and merge
those changes into their own repositories if they like.  All of this
can flow naturally to one or more "master" public repositories which
represent some group of people's best idea of what is true and valuable
from everyone's contributions.  By using Git for this process we can
take advantage of its automatic recording of the complete history of
who contributed what, as well as its powerful tools for branching,
merging, and collaborating across networks, and excellent
community hosting services like Github.


Why use Restructured Text?
--------------------------

Restructured Text is a minimal markup language that anyone can learn
quickly by looking at example documents.  More to the point, it has been
adopted for many documentation projects and has a wide variety of
wonderful tools, such as ``docutils`` and ``sphinx``.  It has many
advantages:

* it is an open, standard format.  Your content will never be
  "trapped" in restructured text; you can convert it to almost anything.

* it can be compiled to many output formats such as HTML, XML, Latex etc.
  using ``sphinx``.

* it can work easily with equations via its support for Latex output
  and jsMath for HTML.

* it can be published easily either as stand-alone HTML or uploaded
  automatically to software like WordPress.

* as a line-oriented format, it works beautifully with Git.

Replace Closed Formats with Open Formats
----------------------------------------

Ownership means *control*: the ability to do what you want with content
that you've written.  If you can't re-use your content for many different
purposes easily, you don't really have that control.  If your content is
trapped in unwieldy, closed formats such as Microsoft Word, can you
truly say that you *own* your own words?  In working with Gitpublish,
I am moving my content to the following open formats that it can work
with easily in a variety of ways (see :doc:`basic`):

* *Word processing / text formats*: convert to restructured text.  Gitpublish
  provides some very basic tools for that, but this is sure to be a growing
  category over time.

* *Tables and spreadsheets*: convert to CSV.  Spreadsheet programs
  can work natively with CSV format data.  As a line-oriented format,
  it "plays nice" with Git.  Restructured text can display CSV files
  directly using its ``csv-table`` directive.

* *Outlines*: convert to OPML, a standard XML format for outlines.
  Gitpublish can automatically generate restructured text from OPML,
  so you can keep your outlines in OPML, which "plays nice" with Git.

Try Gitpublish Yourself
--------------------

You obviously need git to use Gitpublish in any meaningful way.  You 
can get it from [http://git-scm.com/].

You can either get a copy of Gitpublish directly::

   git clone git://github.com/cjlee112/gitpublish.git

Or better yet, create your own fork of Gitpublish on Github.  Go to
[http://github.com/cjlee112/gitpublish] and click the ``fork`` button.
Then clone it to your local computer via::

   git clone git@github.com:username/gitpublish.git
   cd Gitpublish
   git remote add upstream git://github.com/cjlee112/gitpublish.git

where *username* should be your Github user name.

You can then, edit, commit, and branch Gitpublish to your heart's content.
The wiki documents are in the ``doc`` directory, and the source code
in the ``gitpublish`` directory.

If you cloned the repository from your own fork, you can then push your changes
to your public Github repository::

   git push origin master

(if you want to push a branch other than *master* substitute its name here).
Send me a pull request via Github if you want me to merge some of your changes
to my "master" version of Gitpublish.  Your changes will show up in the "master"
version stamped with your authorship and history information; any copy 
of the repository then shows the complete history of everyone who contributed
to it!

To fetch the latest changes from my repository::

   git fetch upstream

You could then merge my latest ``master`` branch to your current branch via::

   git merge remotes/upstream/master

For a graphical view of the latest changes and branches::

   gitk --all 

For my Git cheatsheet with links to more info on Git, see
[http://code.google.com/p/pygr/wiki/UsingGit].

Generating HTML Output
----------------------

For generating HTML output you need several pieces of software installed:

* Python

* docutils

* sphinx

With these installed, generating HTML is as easy as::

   cd doc
   make html

The HTML output will show up in ``doc/_build/html``.

Importing Your Data
-------------------

Gitpublish provides some basic tools for importing a variety of data
formats.  See :doc:`basic`.


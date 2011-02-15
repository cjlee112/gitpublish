
==================================================================
Gitpublish: Using Git and Restructured Text as a Publishing System
==================================================================

Goals
-----

I want the freedom to use the best tool for each distinct function
in the publishing process, and have them work together easily:

* **open, standard formats** that can be edited and viewed using many
  excellent tools;

* **collaboration tools** and **version control** using the fantastic
  capabilities of **git** and similar software.

* **easily publish** the same content **to any open, standard 
  publishing platform** like WordPress, LaTex, Sphinx etc.,
  or to different publishing / sharing services like Google Docs.

* **work across different devices with easy synchronization**
  so you can edit & view documents on computers, smartphone,
  iPad etc. and immediately synchronize your work across your
  different devices -- without having to hand your documents
  to some third-party.

* support essential capabilities like **equations**, **bibliographic
  databases**, inter-document and external links, across platforms.

Ownership means *control*: the ability to do whatever you want with
your work.  I don't want to be trapped in one particular format or
platform that claims to solve all problems.  I've experienced enough
of that (e.g. Microsoft Office) and can already say that based
on my experience with Gitpublish and associated open tools, I'll
never go back.  I can get what I want done so much more easily,
and the results look and work far better.  Can *you* publish straight
from MS Word to WordPress?  Gitpublish can do it with a single command.
Can *you* edit and view a complex document with sophisticated
equations and figures on your iPad, and from there
publish that document both to a remote
WordPress blog and to beautifully LaTex'd hardcopy?  This is
easy to do within Gitpublish and the open source publishing ecosystem.

What can Gitpublish do?
-----------------------

* write your content once, using standard, open formats like
  reStructured Text, and whatever editing tools you want.

* manage your document(s) history and collaborate with others on it
  using the incredibly powerful, convenient capabilities of
  git.

* Add external publishing channels like WordPress as git "remote repositories"
  that gitpublish can "push" your content to completely automatically --
  including any necessary format transformations.

This puts *you* in control of your publishing process.  Your collaborator
wants a bunch of changes *after* you published "the final version"?
No problem: pull his changes using git, merge into your publishing branch,
and just re-push the new state of that branch to your remote publishing
channel.  Gitpublish makes these external publishing channels act like
"just another remote repository" that git can push to (and fetch from, 
if the external channel supports that).

Who is this good for?
---------------------

You might like Gitpublish if

* you like open document formats such as reStructured Text or LaTex.

* you're familiar with open-source tools such as git and Python.

* you're looking for a way to view and edit documents with equations
  on your iPad, iPhone or iPod Touch (I still haven't found a way
  to install git or even mercurial on Android, grr).

Warning: This is a very early developer-version with limited capabilities and
testing, so only try it at your own risk.  Since Gitpublish mainly
works by running git commands, it cannot corrupt your git repository,
and every step of your work will be captured in the git commit history.
So you are unlikely to lose data or work, I think.

For a simple tutorial on using Gitpublish, take a look at :doc:`tutorials/intro`.

Why use Git for publishing?
---------------------------

Git is the swiss army knife of content control.  It makes it trivial
to work on the same content on a variety of different devices without
every having to think about "wait, which device has the latest revision?"
or "oops, I made different changes on different devices, how do I merge them?"
Version history, backup, synchronization, merging -- those are Git's
*trivial* capabilities.  Even if you're working completely by yourself,
git is a life-changing tool that gives you amazing new ways to work
(I could go on for hours about how often I use Git branching to keep
multiple lines of development for trying out different ideas on
the same project...).

Moreover, distributed version control systems like Git solve one of the basic 
problems of collaborating on text projects 
-- how to let everyone have autonomy (i.e. edit their
version of some content as they like), while sharing with others.
Each user can have their own copy, edit it however they like,
but then make their changes available to others, who can pull and merge
those changes into their own repositories *if* they like them.  All of this
can flow naturally to one or more "master" public repositories which
represent some group of people's best idea of what is true and valuable
from everyone's contributions.  By using Git for this process we can
take advantage of its automatic recording of the complete history of
who contributed what, as well as its powerful tools for branching,
merging, and collaborating across networks, and excellent
community hosting services like `Github <http://github.com>`_.


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

Getting Gitpublish
------------------

Gitpublish requires both `Python <http://python.org>`_ and 
`git <http://git-scm.com/>`_.  You also need 
`Docutils <http://docutils.sourceforge.net/>`_ and
`Sphinx <http://sphinx.pocoo.org/>`_ is strongly recommended.

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


Importing Your Data
-------------------

Gitpublish provides some basic tools for importing a variety of data
formats.  See :doc:`tools`.


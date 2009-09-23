
===============================================================
Gitwiki: Using Git and Restructured Text as a Publishing System
===============================================================

Why use Git for a Wiki?
-----------------------

Distributed version control systems like Git solve one of the basic 
problems of wikis -- how to let everyone have autonomy (i.e. edit their
version of some content as they like), while sharing with others.
Each user can have their own copy of the wiki, edit it however they like,
but then make their changes available to others, who can pull and merge
those changes into their own repositories if they like.  All of this
can flow naturally to one or more "master" public repositories which
represents some group of people's best idea of what is true and valuable
from everyone's contributions.  By using Git for this process we can
take advantage of its automatic recording of the complete history of
who contributed what, as well as its powerful tools for branching,
merging, and collaborating across networks, as well as excellent
community hosting services like Github.


Why use Restructured Text for a Wiki?
-------------------------------------

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

Ownership means control: the ability to do what you want with content
that you've written.  If you can't re-use your content for many different
purposes easily, you don't really have that control.  If your content is
trapped in unwieldy, closed formats such as Microsoft Word, can you
truly say that you *own* your own words?  In working with Gitwiki,
I am moving my content to the following open formats that it can work
with easily in a variety of ways:

* *Word processing / text formats*: convert to restructured text.  Gitwiki
  provides some very basic tools for that, but this is sure to be a growing
  category over time.

* *Outlines*: convert to OPML, a standard XML format for outlines.
  Gitwiki can automatically generate restructured text from OPML,
  so you can keep your outlines in OPML, which "plays nice" with Git.

* *Tables and spreadsheets*: convert to CSV.  Spreadsheet programs
  can work natively with CSV format data.  As a line-oriented format,
  it "plays nice" with Git.  Restructured text can display CSV files
  directly using its ``csv-table`` directive.

Try Gitwiki Yourself
--------------------

Get a copy of Gitwiki::

   git clone git://github.com/cjlee112/Gitwiki.git


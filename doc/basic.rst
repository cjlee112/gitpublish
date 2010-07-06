
=================
Gitwiki Functions
=================

.. module:: basic
   :synopsis: Functions for importing and publishing text using Git
.. moduleauthor:: Christopher Lee <leec@chem.ucla.edu>
.. sectionauthor:: Christopher Lee <leec@chem.ucla.edu>

**This info is pretty obsolete**: 
for a better intro, see `this tutorial <tutorials/intro.html>`_

This module supplies convenience functions for importing from 
MoinMoin, OPML, some simple text formats, etc., and for exporting to
HTML, Latex, and WordPress.

Converting Simple Text to Restructured Text
-------------------------------------------

Gitwiki provides a basic utility for converting a plain-text, 
non-line-wrapped input to restructured text.
This trivial reformatter is suitable for text copied from a word
processing document, i.e. it applies text-wrapping to produce
a basic reST format.  It follows a few simple rules:

* lines starting with '*' are treated as list items.

* lines that contain a colon (or any headerMark you specify)
  are treated as section headers, if the headerMark occurs up to
  a specified position in the line (headerMax)

* the first section header is treated as the Document Title, up to
  the colon (or headerMark).

* other lines are treated as paragraphs, and are line-wrapped, with
  an extra blank line inserted between paragraphs.

Use it as follows::

   >>> textFile = file('myfile.txt')
   >>> restFile = file('myfile.rst', 'w')
   >>> basic.simpletext_to_rest(textFile, restFile, 
                                headerMark=':', headerMax=40)
   ...
   >>> textFile.close()
   >>> restFile.close()

Converting OPML to Restructured Text
------------------------------------

OPML is a convenient format for outlining.  Tools like Omni Outliner
treat it like a native format for reading and writing, but OPML can
be checked into git directly, since it's a line-based format.
For displaying these outlines on the webor other publishing formats, 
it is convenient to convert
the OPML to restructured text, and thence to HTML or Latex.

Currently, this converts two column OPML outlines into
a simple restructured text list with nested indentation matching the
outline levels.  Each outline item is presented in the format
*column1*: column2, where column1 is assumed to be a "short synopsis
phrase", and column2 is assumed to be a text note expanding on that
topic.  By default, gitwiki looks for a column labeled ``Comment`` as column2,
but you can change that, by passing the ``commentAttr="somecolumn"``
keyword argument to any of the OPML conversion functions.
It also extracts the outline title from the OPML, and uses this
as the title for the restructured text output.

You can convert a set of OPML files on the command line::

   python basic.py --opmlfiles *.opml

This simply produces a series of ``.rst`` files for each of the 
OPML files.

You can convert a single OPML file::

   >>> opmlPath = 'foo.opml'
   >>> restFile = file('foo.rst', 'w')
   >>> basic.convert_opml_to_rest(opmlPath, restFile)
   >>> restFile.close()

or a whole set of files::

   >>> opmlfiles = ['foo.opml', 'bar.opml']
   >>> basic.convert_opml_files(opmlfiles)



Importing from MoinMoin
-----------------------

Gitwiki provides some basic tools for importing the content and history
of a MoinMoin wiki into restructured text stored in a Git repository.

You can import the whole history with a single call::

   basic.commit_moin_by_time(wikiDir, destDir)

* *wikiDir* should be a string path to the MoinMoin pages 
  directory you want to import.  This is typically ``wiki/data/pages``
  inside your MoinMoin install.

* *destDir* should be a directory inside a git repository where
  you want to save the files.

The pages will be imported by converting to restructured text, and
appending the suffix ``.rst`` to the file name.  Each revision is
checked into git, in the order it was created, with a commit message that 
gives the date and time the revision was created in MoinMoin.


Publishing to WordPress
-----------------------

Basic usage: to publish a ReST file to wordpress::

    >>> tab = basic.WordPressBlog('somewhere.wordpress.com',
                                  'somebody', 'apassword')
    >>> tab.post_rest('dollar_phone_plan.rst')
    34

It returns the post_id of the new post, which you can access via:
``http://somewhere.wordpress.com/?p=34``
Note that the new post is created *unpublished* so you will only
be able to see it if you are logged in to your wordpress blog.
You can then publish it from the the WP admin interface.


#! /usr/bin/env python
#
# Generate an HTML Snippet for WordPress Blogs from reStructuredText.
#
# This is a modification of the standard HTML writer that leaves out
# the header, the body tag, and several CSS classes that have no use
# in wordpress. What is left is an incomplete HTML document suitable
# for pasting into the WordPress online editor.
#
# Note: This is a quick hack, so it probably won't work for the more
#       advanced features of rst.
#
# Copyright (c) 2008 Matthias Friedrich <matt@mafr.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the Artistic License.
#
# Modified to support direct output of math and displaymath a la sphinx
# to Blogger, for rendering with MathJax: latex equations are
# embedded either in \( \) (inline) or \[ \] (displaymath) for MathJax
# to render in the web browser.
# -- CJL
import sys
import docutils
from docutils.writers import html4css1
from docutils import frontend, writers, nodes, utils
from docutils.core import publish_cmdline, default_description
from docutils.parsers.rst import directives, roles
from sphinx.ext.mathbase import MathDirective, math, eq_role, \
     displaymath
from sphinx.util.compat import directive_dwim

backslashString = '\\'

class MathDirective2(MathDirective):
	'removes one line from MathDirective that crashes'
	def run(self):
		latex = '\n'.join(self.content)
		if self.arguments and self.arguments[0]:
			latex = self.arguments[0] + '\n\n' + latex
		node = displaymath()
		node['latex'] = latex
		node['label'] = self.options.get('label', None)
		node['nowrap'] = 'nowrap' in self.options
		ret = [node]
		if node['label']:
			tnode = nodes.target('', '', ids=['equation-' + node['label']])
			self.state.document.note_explicit_target(tnode)
			ret.insert(0, tnode)
		return ret


def math_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
	latex = text.replace('\x00', backslashString) # WP strips single backslash
	obj = math(latex=latex)
	obj.document = inliner.document # docutils crashes w/o this
	return [obj], []

def setup():
	'add support for math to docutils'
	nodes._add_node_class_names(['math', 'displaymath', 'eqref'])
	roles.register_local_role('math', math_role)
	roles.register_local_role('eq', eq_role)
	directives.register_directive('math', directive_dwim(MathDirective2))

class Writer(html4css1.Writer):
	supported = ('wphtml', )

	settings_spec = html4css1.Writer.settings_spec + ( )

	def __init__(self, doc=None, unresolvedRefs=None, klass=None):
		html4css1.Writer.__init__(self)
		if klass is None:
			klass = HtmlTranslatorBase
		class MyWpHtmlTranslator(klass):
			gitpubDoc = doc
			gitpubUnresolvedRefs = unresolvedRefs
		self.translator_class = MyWpHtmlTranslator


class HtmlTranslatorBase(html4css1.HTMLTranslator):
	"""An HTML emitting visitor.

	Assumes your WP has support for jsMath."""

	doctype = ('')

	def __init__(self, *args):
		html4css1.HTMLTranslator.__init__(self, *args)
		self.stylesheet = [ ]
		self.meta = [ ]
		self.head = [ ]
		self.head_prefix = [ ]
		self.body_prefix = [ ]
		self.body_suffix = [ ]
		self.section_level = 3
		self.compact_simple = True
		self.literal_block = False
		self.skip_document_title = False


	def visit_document(self, node):
		pass

	def depart_document(self, node):
		pass

	def visit_section(self, node):
		self.section_level += 1

	def depart_section(self, node):
		self.section_level -= 1

	def visit_reference(self, node):
		attrs = { }
		if node.has_key('refuri'):
			attrs['href'] = node['refuri']
		else:
			assert node.has_key('refid'), 'Invalid internal link'
			attrs['href'] = '#' + node['refid']
		self.body.append(self.starttag(node, 'a', '', **attrs))

	def visit_Text(self, node):
		if self.literal_block:
			text = node.astext()
		else:
			text = node.astext().replace('\n', ' ')
		encoded = self.encode(text)
		if self.in_mailto and self.settings.cloak_email_addresses:
			encoded = self.cloak_email(encoded)
		self.body.append(encoded)

	def visit_block_quote(self, node):
		self.body.append('\n')

	def depart_block_quote(self, node):
		self.body.append('\n')

	def visit_list_item(self, node):
		self.body.append('  ' + self.starttag(node, 'li', ''))

	def visit_title(self, node):
		if isinstance(node.parent, nodes.document): # doc title
			self.skip_document_title = True
			self.skip_document_start = len(self.body)
			return # title passed as metadata, don't repeat it here
		h_level = self.section_level + self.initial_header_level - 1
		self.body.append(
			self.starttag(node, 'h%s' % h_level, '', **{ }))
		self.context.append('</h%s>\n\n' % (h_level, ))

	def depart_title(self, node):
		if self.skip_document_title:
			del self.body[self.skip_document_start:]
			self.skip_document_title = False
		else:
			self.body.append(self.context.pop())

	def visit_literal_block(self, node):
		self.literal_block = True
		self.body.append(self.starttag(node, 'pre'))

	def depart_literal_block(self, node):
		self.body.append('\n</pre>\n\n')
		self.literal_block = False

	def visit_literal(self, node):
		self.body.append('<code>')

	def depart_literal(self, node):
		self.body.append('</code>')

	def visit_math(self, node):
		self.body.append(r'\(' + self.encode(node['latex'])
				 + r'\)')
		raise nodes.SkipNode
		
	def visit_displaymath(self, node):
		self.body.append(r'\[' + self.encode(node['latex'])
				 + r'\]')
		raise nodes.SkipNode

	# overwritten
	def visit_image(self, node):
		'''rewrite local path to its path on remote, or if that
		fails, add document to unresolved refs list.'''
		try:
			d = self.gitpubDoc.relative_path(node['uri'])
			node['uri'] = d['gitpubRemotePath'] # use path on remote
		except KeyError: # not yet present in mapping, so resolve later
			self.gitpubUnresolvedRefs.add(self.gitpubDoc)
		except TypeError: # no docmap?
			pass
		html4css1.HTMLTranslator.visit_image(self, node)

class WpHtmlTranslator(HtmlTranslatorBase):
	'WP does not like <P>foo</P> ??'
	def visit_paragraph(self, node):
		if self.should_be_compact_paragraph(node):
			self.context.append('')
		else:
			self.body.append('')
			self.context.append('\n\n')

		
if __name__ == '__main__':
	# docutils tries to load the module 'wphtml' below, so we need an alias
	sys.modules['wphtml'] = sys.modules['__main__']

	try:
	    import locale
	    locale.setlocale(locale.LC_ALL, '')
	except:
	    pass

	description = ('Generates an HTML Snippet for Wordpress from'
			'standalone reStructuredText sources.  '
			+ default_description)

	publish_cmdline(writer_name='wphtml', description=description)

# EOF

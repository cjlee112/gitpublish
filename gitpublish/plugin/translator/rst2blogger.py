# Modified to support direct output of math and displaymath a la sphinx
# to Blogger, for rendering with MathJax: latex equations are
# embedded either in \( \) (inline) or \[ \] (displaymath) for MathJax
# to render in the web browser.
# -- CJL
import rst2wp

class Writer(rst2wp.Writer):
	'make the writer use our translator class'
	def __init__(self, *args, **kwargs):
		kwargs['klass'] = BloggerTranslator
		rst2wp.Writer.__init__(self, *args, **kwargs)

class BloggerTranslator(rst2wp.HtmlTranslatorBase):
	def visit_math(self, node):
		self.body.append(r'\(' + self.encode(node['latex'])
				 + r'\)')
		raise nodes.SkipNode
		
	def visit_displaymath(self, node):
		self.body.append(r'\[' + self.encode(node['latex'])
				 + r'\]')
		raise nodes.SkipNode

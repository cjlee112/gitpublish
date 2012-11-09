import xmlrpclib
from docutils.core import publish_string
from translator import html2rest, rst2blogger
from StringIO import StringIO
import os.path
from gitpublish import core
try:
    import gdata.blogger.client
    import gdata.blogger.data
    import atom.data
except ImportError:
    raise ImportError('''blogger plugin requires gdata and atom packages
    Please install them!''')

class Repo(core.RepoBase):
    'standard interface to a Blogger blog'
    def __init__(self, host, user, password=None, blog_id=0):
        'for blogger service, host arg is ignored'
        core.RepoBase.__init__(self, host, user, password, blog_id)
        self.client = gdata.blogger.client.BloggerClient()

    def check_password(self, attr='password'):
        core.RepoBase.check_password(self, attr)
        if attr == 'password' and not hasattr(self, 'logged_in'):
            self.client.client_login(
                self.user, self.password,
                source='leec-gitpublish-0.1',
                service='blogger')
            self.logged_in = True
            

    def new_post(self, title, content, publish=True):
        'create post with specified title and HTML content'
        post = self.client.add_post(self.blog_id, title, content,
                                    draft=not publish)
        return post.get_post_id()

    def new_page(self, title, content, publish=True):
        'create page with specified title and HTML content'
        page = self.client.add_page(self.blog_id, title, content,
                                    draft=not publish)
        return page.get_page_id()

    def get_blog(self):
        'get blog object for this blog'
        try:
            return self.blog
        except AttributeError:
            feeds = self.client.get_blogs()
            for blog in feeds.entry:
                if blog.get_blog_id() == str(self.blog_id):
                    self.blog = blog
                    return blog
        raise ValueError('no blog matching blog_id??')

    def _find_post(self, post_id):
        'get post object for specified post'
        blog = self.get_blog()
        post = self.client.get_feed(
            blog.get_post_link().href + '/%s' % post_id,
            auth_token=self.client.auth_token,
            desired_class=gdata.blogger.data.BlogPost)
        return post

    def update_post(self, post_id, title, content, publish=True):
        'update with new title and content'
        post = self._find_post(post_id)
        post.title = atom.data.Title(title)
        post.content = atom.data.Content(content)
        return self.client.update(post)

    def get_post_list(self, maxposts=2000):
        'maxposts ignored currently...'
        feed = self.client.get_posts(self.blog_id)
        return feed.entry
    
    def get_page_list(self, maxpages=2000):
        'maxpages ignored currently...'
        feed = self.client.get_pages(self.blog_id)
        return feed.entry
    
    def _find_page(self, page_id):
        'get page object for specified page'
        for page in self.get_page_list():
            if page.get_page_id() == page_id:
                return page
        raise ValueError('no page matching page_id??')

    def update_page(self, page_id, title, content, publish=True):
        'update with new title and content'
        page = self._find_page(page_id)
        page.title = atom.data.Title(title)
        page.content = atom.data.Content(content)
        return self.client.update(page)
        
    def delete_post(self, post_id):
        'delete specified post'
        post = self.get_post(post_id)
        self.client.delete(post)

    def delete_page(self, page_id):
        'delete specified page'
        page = self.get_page(page_id)
        self.client.delete(page)

    def get_page(self, page_id):
        'get HTML and attr dictionary for this page'
        page = self._find_page(page_id)
        html = page.content.text
        return html, dict(title=page.title.text)

    def get_post(self, post_id):
        'get HTML and attr dictionary for this post'
        post = self._find_post(post_id)
        html = post.content.text
        return html, dict(title=post.title.text)
        
    def convert_rest(self, doc, unresolvedRefs=None):
        'convert ReST to Blogger html using docutils, rst2blogger'
        writer = rst2blogger.Writer(doc, unresolvedRefs)
        return publish_string(doc.rest, writer=writer, # convert to wordpress
                              settings_overrides=dict(report_level=5))


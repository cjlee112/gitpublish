import xmlrpclib
from docutils.core import publish_string
from translator import html2rest, rst2wp
from gitpublish import core
import warnings

class Repo(core.RepoBase):
    def __init__(self, host, user, password=None, blog_id=0, path='/xmlrpc.php',
                 appkey=None):
        core.RepoBase.__init__(self, host, user, password, blog_id)
        url = 'http://' + host + path
        self.server = xmlrpclib.ServerProxy(url)
        self.path = path
        self.appkey = appkey

    def new_post(self, title, content, publish=True):
        'create post with specified title and HTML content'
        d = dict(title=title, description=content)
        return self.server.metaWeblog.newPost(self.blog_id,
                    self.user, self.password, d, publish)

    def new_page(self, title, content, publish=True):
        'create page with specified title and HTML content'
        d = dict(title=title, description=content)
        return self.server.wp.newPage(self.blog_id, self.user,
                                      self.password, d, publish)

    def get_page(self, page_id):
        'get HTML and attr dictionary for this page'
        result = self.server.wp.getPage(self.blog_id, page_id, self.user,
                                        self.password)
        html = result['description']
        del result['description'] # don't duplicate the content
        return html, result

    def get_post(self, post_id):
        'get HTML and attr dictionary for this post'
        result = self.server.metaWeblog.getPost(pub_id, self.user,
                                                self.password)
        html = result['description'] + result['mt_text_more']
        del result['description'] # don't duplicate the content
        del result['mt_text_more']
        return html, result
    
    def update_page(self, page_id, title, content, publish=True):
        'update with new title and content'
        d = dict(title=title, description=content)
        return self.server.wp.editPage(self.blog_id, page_id, self.user,
                                       self.password, d, publish)

    def update_post(self, post_id, title, content, publish=True):
        'update with new title and content'
        d = dict(title=title, description=content)
        try:
            v = self.server.metaWeblog.editPost(post_id, self.user,
                                                self.password, d, publish)
        except xmlrpclib.ResponseError:
            v = self.server.wp.editPost(self.blog_id, self.user,
                                        self.password, post_id,
                                        dict(post_title=title,
                                             post_content=content))
        return v
    
    def delete_page(self, page_id):
        'delete specified page'
        return self.server.wp.deletePage(self.blog_id, self.user,
                                         self.password, page_id)

    def delete_post(self, post_id, publish=True):
        'delete specified post'
        self.check_password('appkey') # does WP really require this?
        return self.server.blogger.deletePost(self.appkey, post_id,
                                              self.user, self.password,
                                              publish)

    def delete_file(self, doc_id):
        warnings.warn('wordpress lacks file deletion function... ignoring.')
        return True # don't treat as XMLRPC error

    def get_post_list(self, maxposts=2000):
        return self.server.metaWeblog.getRecentPosts(self.blog_id,
                    self.user, self.password, maxposts)

    def get_page_list(self, maxpages=2000):
        'maxpages ignored currently...'
        return self.server.wp.getPageList(self.blog_id, self.user,
                                          self.password)
    
    def convert_rest(self, doc, unresolvedRefs=None):
        'convert ReST to WP html using docutils, rst2wp'
        writer = rst2wp.Writer(doc, unresolvedRefs)
        return publish_string(doc.rest, writer=writer, # wordpress format
                              settings_overrides=dict(report_level=5))



    

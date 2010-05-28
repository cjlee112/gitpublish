import xmlrpclib
from docutils.core import publish_string
from translator import html2rest, rst2wp
from StringIO import StringIO


class Repo(object):
    def __init__(self, host, user, password, blog_id=0, path='/xmlrpc.php'):
        url = 'http://' + host + path
        self.server = xmlrpclib.ServerProxy(url)
        self.host = host
        self.user = user
        self.password = password
        self.blog_id = int(blog_id)
        self.path = path

    def new_document(self, doc, pubtype='post', publish=True, gitpubHash=None,
                     *args, **kwargs):
        'post a restructured text file to wordpress as post or page'
        html = convert_rest_to_wp(str(doc))
        if gitpubHash: # insert our hash code as HTML comment
            html += '\n<!-- gitpubHash=%s -->\n' % gitpubHash
        d = dict(title=doc.title, description=html)
        if pubtype == 'page':
            return 'page' + self.server.wp.newPage(self.blog_id, self.user,
                                             self.password, d, publish)
        else:
            return 'post' + self.server.metaWeblog.newPost(self.blog_id,
                                 self.user, self.password, d, publish)

    def get_document(self, doc_id):
        'retrieve the specified post or page and convert to ReST'
        pubtype, pub_id = doc_id[:4], doc_id[4:]
        if pubtype == 'page':
            result = self.server.wp.getPage(self.blog_id, pub_id, self.user,
                                            self.password)
            html = result['description']
        else:
            result = self.server.metaWeblog.getPost(pub_id, self.user, self.password)
            html = result['description'] + result['mt_text_more']
            del result['mt_text_more']
        del result['description'] # don't duplicate the content
        try: # extract our hash code if present
            i = html.index('gitpubHash=') + 11 # start of hash code
            result['gitpubHash'] = html[i:i + 100].split()[0]
        except ValueError:
            pass
        buf = StringIO()
        parser = html2rest.Parser(buf)
        parser.feed(html)
        parser.close()
        rest = buf.getvalue()
        return rest, result
            
    def set_document(self, doc_id, doc, publish=True, gitpubHash=None, *args, **kwargs):
        'post a restructured text file to wordpress as the specified doc_id'
        pubtype, pub_id = doc_id[:4], doc_id[4:]
        html = convert_rest_to_wp(str(doc))
        if gitpubHash: # insert our hash code as HTML comment
            html += '\n<!-- gitpubHash=%s -->\n' % gitpubHash
        d = dict(title=doc.title, description=html)
        if pubtype == 'page':
            v = self.server.wp.editPage(self.blog_id, pub_id,
                                        self.user, self.password, d, publish)
        else:
            v = self.server.metaWeblog.editPost(pub_id, self.user, self.password,
                                                d, publish)
        if not v:
            raise ValueError('xmlrpc server method failed: check your args')

    def delete_document(self, doc_id, publish=True, *args, **kwargs):
        'delete a post or page from the WP server'
        pubtype, pub_id = doc_id[:4], doc_id[4:]
        if pubtype == 'page':
            v = self.server.wp.deletePage(self.blog_id, self.user,
                                          self.password, pub_id)
        else:
            v = self.server.blogger.deletePost(self.appkey, pub_id, self.user,
                                               self.password, publish)
        if not v:
            raise ValueError('xmlrpc server method failed: check your args')

    def list_documents(self, maxposts=2000):
        'get list of posts and pages from server, return as dictionary'
        d = {}
        l = self.server.metaWeblog.getRecentPosts(self.blog_id, self.user,
                                                  self.password, maxposts)
        for kwargs in l:
            d['post' + str(kwargs['postid'])] = kwargs
        l = self.server.wp.getPageList(self.blog_id, self.user, self.password)
        for kwargs in l:
            d['page' + str(kwargs['page_id'])] = kwargs
        return d

        
    
def convert_rest_to_wp(rest):
    'convert ReST to WP html using docutils, rst2wp'
    writer = rst2wp.Writer()
    return publish_string(rest, writer=writer) # convert to wordpress



    

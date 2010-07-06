import xmlrpclib
from docutils.core import publish_string
from translator import html2rest, rst2wp
from StringIO import StringIO
import os.path
from gitpublish import core
from getpass import getpass


class Repo(object):
    def __init__(self, host, user, password=None, blog_id=0, path='/xmlrpc.php',
                 appkey=None):
        url = 'http://' + host + path
        self.server = xmlrpclib.ServerProxy(url)
        self.host = host
        self.user = user
        self.password = password
        self.blog_id = int(blog_id)
        self.path = path
        self.appkey = appkey

    def check_password(self, attr='password'):
        'ask user for password if not already stored'
        if getattr(self, attr, None) is None:
            setattr(self, attr, getpass('Enter %s for %s on %s:' %
                                        (attr, self.user, self.host)))

    def new_document(self, doc, pubtype='post', publish=True, gitpubHash=None,
                     unresolvedRefs=None, *args, **kwargs):
        'post a restructured text file to wordpress as post or page'
        self.check_password()
        if hasattr(doc, 'rest'):
            html = convert_rest_to_wp(doc, unresolvedRefs)
        else:
            return self.upload_file(doc)
        if gitpubHash: # insert our hash code as HTML comment
            html += '\n<!-- gitpubHash=%s -->\n' % gitpubHash
        d = dict(title=doc.title, description=html)
        if pubtype == 'page':
            gitpubID = 'page:' + str(self.server.wp.newPage(self.blog_id, self.user,
                                                        self.password, d, publish))
        else:
            gitpubID = 'post:' + self.server.metaWeblog.newPost(self.blog_id,
                                 self.user, self.password, d, publish)
        return dict(gitpubID=gitpubID, gitpubRemotePath='/?p=' + gitpubID[5:])

    def upload_file(self, doc, doc_id=None):
        'upload file to WP server for inclusion in documents'
        if doc_id:
            wpName = doc_id.split('/')[-1]
            if wpName.startswith('wpid-'):
                wpName = wpName[5:]
        else:
            wpName = os.path.basename(doc.gitpubPath)
        content = dict(name=wpName, type=doc.contentType,
                       bits=xmlrpclib.Binary(doc.binaryData), overwrite=True)
        result = self.server.wp.uploadFile(self.blog_id, self.user, self.password,
                                           content)
        gitpubRemotePath = '/' + '/'.join(result['url'].split('/')[3:])
        return dict(gitpubID='file:' + gitpubRemotePath,
                    gitpubRemotePath=gitpubRemotePath,
                    gitpubUnlisted=True) # WP only lists pages & posts, not files

    def _get_pubtype_id(self, doc_id):
        pubtype = doc_id.split(':')[0]
        pub_id = doc_id[len(pubtype) + 1:]
        return pubtype, pub_id

    def get_document(self, doc_id):
        'retrieve the specified post or page and convert to ReST'
        self.check_password()
        pubtype, pub_id = self._get_pubtype_id(doc_id)
        if pubtype == 'page':
            result = self.server.wp.getPage(self.blog_id, pub_id, self.user,
                                            self.password)
            html = result['description']
        elif pubtype == 'post':
            result = self.server.metaWeblog.getPost(pub_id, self.user, self.password)
            html = result['description'] + result['mt_text_more']
            del result['mt_text_more']
        else:
            raise ValueError('no method to get pubtype: %s' % pubtype)
        del result['description'] # don't duplicate the content
        try: # extract our hash code if present
            i = html.index('gitpubHash=')
            result['gitpubHash'] = html[i + 11:i + 100].split()[0]
            j = html[i:].index('>')
            html = html[:i-5] + html[i + j + 1:] # remove inserted comment
        except ValueError:
            pass
        buf = StringIO()
        parser = html2rest.Parser(buf)
        parser.feed(html)
        parser.close()
        rest = buf.getvalue()
        doc = core.Document(rest=rest)
        result['gitpubRemotePath'] = '/?p=' + pub_id
        return doc, result
            
    def set_document(self, doc_id, doc, publish=True, gitpubHash=None,
                     unresolvedRefs=None, *args, **kwargs):
        'post a restructured text file to wordpress as the specified doc_id'
        self.check_password()
        pubtype, pub_id = self._get_pubtype_id(doc_id)
        if pubtype == 'file':
            return self.upload_file(doc, doc_id)
        html = convert_rest_to_wp(doc, unresolvedRefs)
        if gitpubHash: # insert our hash code as HTML comment
            html += '\n<!-- gitpubHash=%s -->\n' % gitpubHash
        d = dict(title=doc.title, description=html)
        if pubtype == 'page':
            v = self.server.wp.editPage(self.blog_id, pub_id,
                                        self.user, self.password, d, publish)
        elif pubtype == 'post':
            v = self.server.metaWeblog.editPost(pub_id, self.user, self.password,
                                                d, publish)
        else:
            raise ValueError('unknown pubtype: %s' % pubtype)
        if not v:
            raise ValueError('xmlrpc server method failed: check your args')

    def delete_document(self, doc_id, publish=True, *args, **kwargs):
        'delete a post or page from the WP server'
        self.check_password()
        pubtype, pub_id = self._get_pubtype_id(doc_id)
        if pubtype == 'page':
            v = self.server.wp.deletePage(self.blog_id, self.user,
                                          self.password, pub_id)
        elif pubtype == 'post':
            self.check_password('appkey') # does WP really require this?
            v = self.server.blogger.deletePost(self.appkey, pub_id, self.user,
                                               self.password, publish)
        elif pubtype == 'file':
            print 'wordpress lacks file deletion function... ignoring.'
            return
        else:
            raise ValueError('unknown pubtype: %s' % pubtype)
        if not v:
            raise ValueError('xmlrpc server method failed: check your args')

    def list_documents(self, maxposts=2000):
        'get list of posts and pages from server, return as dictionary'
        self.check_password()
        d = {}
        l = self.server.metaWeblog.getRecentPosts(self.blog_id, self.user,
                                                  self.password, maxposts)
        for kwargs in l:
            d['post:' + str(kwargs['postid'])] = kwargs
        l = self.server.wp.getPageList(self.blog_id, self.user, self.password)
        for kwargs in l:
            d['page:' + str(kwargs['page_id'])] = kwargs
        return d

        
    
def convert_rest_to_wp(doc, unresolvedRefs=None):
    'convert ReST to WP html using docutils, rst2wp'
    writer = rst2wp.Writer(doc, unresolvedRefs)
    return publish_string(doc.rest, writer=writer) # convert to wordpress



    

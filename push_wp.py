from gitpublish.plugin.translator import rst2wp
from gitpublish.plugin import wordpress
from gitpublish import core
import sys
import optparse
import getpass


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        '--page', action="store_true", dest="is_page", default=False,
        help='push content as wordpress page instead of wordpress post')
    parser.add_option(
        '--user', action="store", type="string",
        dest="user", default=getpass.getuser(),
        help="wordpress username")
    parser.add_option(
        '--password', action="store", type="string",
        dest="password",
        help="wordpress password")
    parser.add_option(
        '--blog_id', action="store", type="int",
        dest="blog_id", default=0,
        help="wordpress blog_id")
    parser.add_option(
        '--title', action="store", type="string",
        dest="title", default='untitled',
        help="title of document")
    return parser.parse_args()

if __name__ == '__main__':
    options, args = get_options()
    restfile, host = args # required args
    ifile = open(restfile)
    try:
        rest = ifile.read()
    finally:
        ifile.close()
    doc = core.Document(rest=rest)
    doc.title = options.title
    repo = wordpress.Repo(host, options.user, options.password,
                          options.blog_id)
    if options.is_page:
        pubtype = 'page'
    else:
        pubtype = 'post'
    repo.new_document(doc, pubtype)

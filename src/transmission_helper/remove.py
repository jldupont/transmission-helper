"""
    Transmission Remove
    
    - verifies which Torrents are completed i.e. 'seeding' status
    - removes them from the session list
    - optionally creates a symlink to the completed torrents in a user chosen directory
    
    @author: jldupont
    @date: Jul 31, 2010
"""
__all__=["main",]
import os
import sys
try:
    import transmissionrpc
except:
    print "(error) this tool requires 'transmissionrpc' package from pypi"
    sys.exit(1)


def get_client_session(host, port):
    c=transmissionrpc.Client(host, port=port)
    return (c, c.get_session())

def check_symdir(path):
    if os.path.isdir(path):
        return False
    os.mkdir(path)
    return True

def process(download_dir, sym, sym_dir, torrent):
    if not sym:
        return
    src=os.path.join(download_dir, torrent.name)
    link_name=os.path.join(sym_dir, torrent.name)
    os.symlink(src, link_name)
    

def remove(client, id):
    client.remove(id)

## ===================================================================
    

def main():
    from optparse import OptionParser    
    parser = OptionParser()
    parser.add_option("-p", "--port",  dest="port",  help="RPC Port", default=9091)
    parser.add_option("-s", "--sym",   dest="sym",   help="Generate symlinks",      default=True)
    parser.add_option("-d", "--sdir",  dest="sdir",  help="Directory for symlinks", default="~/completed_torrents")
    parser.add_option(      "--host",  dest="host",  help="RPC Host", default="localhost")    
    (options, _args) = parser.parse_args()
    
    sdir=os.path.expanduser(options.sdir)
    
    if options.sym:
        try:
            r=check_symdir(sdir)
            if r:
                print "(info) created '%s'" % sdir
        except:
            print "(error) cannot create directory "
            sys.exit(1)
    try:
        c, s=get_client_session(options.host, options.port)
    except:
        print "(error) cannot get session to Transmission (%s:%s)" % (options.host, options.port)
        sys.exit(1)
        
    dl=s.download_dir
    
    list=c.list()
    for i in list.iterkeys():
        status=list[i].status
        if status=='seeding':
            torrent=list[i]
            print "(info) processing completed: %s" % torrent
            try:    process(dl, options.sym, sdir, torrent)
            except: print "(error) processing: %s" % torrent
            try:    remove(c, i)
            except: print "(error) removing: %s" % torrent

main()

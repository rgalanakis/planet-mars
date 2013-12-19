import argparse
import ftplib
import glob
import os
import shutil
import subprocess
import time


def timestr():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())


def create_files():
    print timestr(), 'Creating files'
    # Using '-m planet' fails under debugger, cannot run __main__
    args = ['python', 'planet\\__main__.py', 'techart/fancy/config.ini']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    print err
    print timestr(), 'Files created.'


def upload_file(ftp, filename):
    with open(filename, 'rb') as f:
        ftp.storbinary('STOR ' + os.path.basename(filename), f)


def get_all_files():
    return glob.glob('techart/output/*.*') + glob.glob('techart/output/images/*.*')


def get_selective_files():
    return ['techart/output/index.html', 'techart/output/rss20.xml']


def upload_files(ftppass):
    print timestr(), 'Beginning upload.'
    ftp = ftplib.FTP('tech-artists.org', 'techftp', ftppass)
    ftp.cwd('planet')
    for f in get_selective_files():
        upload_file(ftp, f)
    ftp.close()
    print timestr(), 'Upload finished.'


def copy_files(tgtdir):
    srcdir = 'techart/output'
    shutil.copytree(srcdir, tgtdir)


def main():
    o = argparse.ArgumentParser()
    o.add_argument('--ftppass')
    o.add_argument('--copyto')
    opts = o.parse_args()
    create_files()
    if opts.copyto:
        print 'Copying output to', opts.copyto
        copy_files(opts.copyto)
    if opts.ftppass:
        print 'Uploading files to FTP.'
        upload_files(opts.ftppass)


if __name__ == '__main__':
    main()

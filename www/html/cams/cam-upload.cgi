#!/usr/bin/env python3
import cgi, os

import cleanup


form = cgi.FieldStorage()
# Get filename here.
print("Content-Type: text/plain\n\n")

fileitem = form['photo']
buf_siz=1024 * 1024 # 1M 

# Test if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    bytes_written=0

    # ensure proper format (host-%Y%m%d%H%M%S
    parts = fn.split('-')
    if len(parts) != 2:
        raise ValueError("error - filename must be label-date")
      
    dest = '/var/www/html/cams/pics/' + fn

    print("reading into " + dest)

    with open(dest, 'wb') as output:
        chunk = fileitem.file.read(buf_siz)
        while chunk:
            output.write(chunk)
            bytes_written += len(chunk)
            print("read %d bytes" % len(chunk))
            chunk = fileitem.file.read(buf_siz)
    print('The file %s of size %d was uploaded successfully' % (dest, bytes_written))
   
    # make small version
    small = '/var/www/html/cams/pics/small/t-' + fn
    os.system('convert ' + dest + ' -adaptive-resize 200x150 ' + small)
    print ('made small version ' + small)

    cleanup.cleanup_files()
else:
   print('No file was uploaded')

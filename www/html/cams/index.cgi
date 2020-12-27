#!/usr/bin/env python3
import cgi, os
import imagefiles

import cgitb; cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html\n\n")

thumbsrel='pics/small'
picsrel='pics'

# format like t-guppy-20201129061054.jpg
print('<html><head><title>Pics</title></head><body>')

print("<p>General format: one column per camera, showing last hour of 5-minute images, then one per hour for 30 hours or so, then one per day as far back as we have.  Click any image to embiggen.</p>")
count=0
print('<table>')

items = imagefiles.all_images()
hosts = sorted(items.keys())
rows=0
print("<tr>")
for host in hosts:
    print("<th>", host, "</th>")
    rows=max(rows, len(items[host]))
print("</tr>")

for rownum in range(rows-1):
    print("<tr>")
    for host in hosts:
        if rownum >= len(items[host]):
            print('<td align="center">no image</td>')
        else:
            thumbfile=items[host][rownum]["thumbfile"]
            imgfile=items[host][rownum]["imgfile"]
            dtobj=items[host][rownum]["timestamp"]
            print('<td align="center">')
            print('<a href="' + picsrel + '/' + imgfile + '" target="bigpic">')
            print('<img src="' + thumbsrel + '/' + thumbfile + '" width="200" height="150" ')
            print('  alt="' + thumbfile + '" />')
            print('</a>')
            print('<br/>' +  dtobj.strftime("%Y-%m-%d %H:%M")) 
            print('</td>')
    print("</tr>")

print('</table>');
print('</body></html>')

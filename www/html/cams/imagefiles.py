#!/usr/bin/env python3
import os
from datetime import datetime,timezone,timedelta

# consider: -normalize -brightness-contrast
# consider: compare adjacent times
# consider: overall brighness to exclude

thumbsdir='/var/www/html/cams/pics/small'
picsdir='/var/www/html/cams/pics'

# map of hostname to list of images, each a hash with
#    imgfile, thumbfile, vidfile, host, timestamp
def all_images():
    hosts={}
    # files formatted like t-guppy-20201129061054.jpg
    for thumbfn in os.listdir(thumbsdir):
        fileinfo={}
        thumbbase = os.path.basename(thumbfn)
        fileinfo["thumbfile"]=thumbbase
        parts = thumbbase.split('-')
        fileinfo["host"] = parts[1]
        datestr = parts[2].split('.')[0]
        dtobj = datetime.strptime(datestr, '%Y%m%d%H%M%S')
        fileinfo["imgfile"] =  fileinfo["host"] + '-' + datestr + '.jpg'
        # convert to pacific
        fileinfo["timestamp"] =  dtobj.replace(tzinfo=timezone.utc).astimezone(tz=timezone(-timedelta(hours=8)))
    
        if fileinfo["host"] in hosts.keys(): 
            files = hosts[fileinfo["host"]]
        else:
            files = []
            hosts[fileinfo["host"]] = files
        files.append(fileinfo)

    for host in hosts.keys():
        hosts[host] = sorted(hosts[host], key=lambda i: (i['timestamp']), reverse=True)

    return hosts

def deleteimage(image):
    os.remove(thumbsdir + '/' + image["thumbfile"])
    os.remove(picsdir + '/' + image["imgfile"])

if __name__ == "__main__":
    # execute only if run as a script
    images = all_images()
    for host in images.keys():
        for image in images[host]:
            print(image["host"], " ", image["timestamp"])

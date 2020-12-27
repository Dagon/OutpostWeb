#!/usr/bin/env python3

import imagefiles

#for each host, keep the latest N images, the latest each hour for a few days, then one from near 10am each day.

def cleanup_files():
    # execute only if run as a script
    items = imagefiles.all_images()
    for host in sorted(items.keys()):
        count=0
        deleted=0
        for image in sorted(items[host], key=lambda i: (i['timestamp']), reverse=True):
            if count < 10:
                # always keep first/newest 10, set the hour counter
                #print("keep", image["host"], " ", image["timestamp"], " (recent)")
                count += 1
                hourkept=image["timestamp"].hour
            elif count < 59:
                # one for each hour
                if image["timestamp"].hour != hourkept:
                    #print("keep", image["host"], " ", image["timestamp"],
                    #    " (hour %d)" % image["timestamp"].hour)
                    count += 1
                    hourkept = image["timestamp"].hour
                    daykept = image["timestamp"].day
                else:
                    print("del",  image["host"], " ", image["timestamp"], "")
                    deleted += 1
                    imagefiles.deleteimage(image)
            else:
                # one for each day
                if image["timestamp"].day != daykept and image["timestamp"].hour == 10:
                    #print("keep", image["host"], " ", image["timestamp"],
                    #    " (day %d)" % image["timestamp"].day)
                    count += 1
                    daykept = image["timestamp"].day
                else:
                    print("del",  image["host"], " ", image["timestamp"], "")
                    deleted += 1
                    imagefiles.deleteimage(image)
        print("kept %d and deleted %d for %s" % (count, deleted, host))

if __name__ == "__main__":
    cleanup_files()

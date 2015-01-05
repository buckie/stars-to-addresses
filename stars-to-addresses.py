# -*- coding: utf-8 -*-
"""
Go to Google Bookmarks: https://www.google.com/bookmarks/

On the bottom left, click "Export bookmarks": https://www.google.com/bookmarks/bookmarks.html?hl=en

After downloading the html file, run this script on it to get the addresses

This script is based on https://gist.github.com/endolith/3896948
"""

from lxml.html import document_fromstring
from geopy.geocoders import Nominatim
import simplekml
import json

from urllib2 import urlopen
import re
import time
import sys

filename = r'GoogleBookmarks.html'

def main():
    with open(filename) as bookmarks_file:
        data = bookmarks_file.read()

    geolocator = Nominatim()

    kml = simplekml.Kml()

    lst = list()

    # Hacky and doesn't work for all of the stars:
    lat_re = re.compile('markers:[^\]]*latlng[^}]*lat:([^,]*)')
    lon_re = re.compile('markers:[^\]]*latlng[^}]*lng:([^}]*)')
    coords_in_url = re.compile('\?q=(-?\d{,3}\.\d*),\s*(-?\d{,3}\.\d*)')

    doc = document_fromstring(data)
    cnt = 0
    for element, attribute, url, pos in doc.body.iterlinks():
        print 'Location #{cnt}'.format(cnt=cnt)

        if 'maps.google' in url:

            description = element.text or ''
            description = description.encode(encoding='utf-8', errors='replace')
            print description
            print u"URL: {0}".format(url)

            if coords_in_url.search(url):
                # Coordinates are in URL itself
                latitude = coords_in_url.search(url).groups()[0]
                longitude = coords_in_url.search(url).groups()[1]
            else:
                # Load map and find coordinates in source of page
                retry_count = 5
                content = None
                while retry_count > 0:
                    try:
                        sock = urlopen(url.replace(' ', '+').encode('UTF8'))
                        content = sock.read()
                        sock.close()
                        break
                    except Exception, e:
                        retry_count -= 1
                        print 'Connection problem:'
                        print repr(e)
                        print 'Waiting 2 minutes and trying again -- {r}'.format(r=retry_count)
                        time.sleep(120)

                time.sleep(3)  # Don't annoy server
                try:
                    latitude = lat_re.findall(content)[0]
                    longitude = lon_re.findall(content)[0]
                except IndexError:
                    print '[Coordinates not found]'
                    print
                    continue

            print latitude, longitude
            retry_count = 5
            location = None

            while retry_count > 0:
                try:
                    location = geolocator.reverse(latitude + ", " + longitude)
                    print location.address
                    break
                except Exception as e:
                    print "Error Encountered: {e}".format(e=e)
                    time.sleep(3)
                    retry_count -= 1

            print
            kml.newpoint(name=description, coords=[(float(longitude), float(latitude))])
            lst.append({'latitude': latitude,
                       'longitude': longitude,
                       'name': description,
                       'url': url.encode(encoding='utf-8', errors='replace'),
                       'address': location.address.encode(encoding='utf-8', errors='replace') if location else 'error'})

            # this is here because there's a tendancy for this script to fail part way through...
            # so at least you can get a partial result
            kml.save("GoogleBookmarks.kml")
            with open('GoogleBookmarks.json', mode='w') as listdump:
                listdump.write(json.dumps(lst))

        cnt += 1
        sys.stdout.flush()

    kml.save("GoogleBookmarks.kml")
    with open('GoogleBookmarks.json', mode='w') as listdump:
        listdump.write(json.dumps(lst))

if __name__ == '__main__':
    main()
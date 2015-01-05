stars-to-addresses
==================

Get addresses from Google starred locations

Dependencies
------------
* Python 2.7
* geopy
* simplekml

Usage
-----

* Export your bookmarks: https://www.google.com/bookmarks/bookmarks.html?hl=en
* Run this script with the downloaded GoogleBookmarks.html on its directory
* Read the output

```
python stars-to-addresses.py > GoogleBookmarks.log &
tail -F GoogleBookmarks.log
```

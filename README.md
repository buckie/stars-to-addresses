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
* Read the output (or use `tee` to make a log file)

```
python stars-to-addresses.py 2>&1 | tee GoogleBookmarks.log
```

# Recursive-Image-Downloader

Downloads all images from a single URL Or recursively downloads all images from all links in the URL.
It follows links recursively up to the level specified.

Make sure you installed [Python3](https://python.org).
Yes that's right, no additional dependencies. Windows compatible (No guarantees whatsoever).
Modify the variables in `Recursive_Image_Downloader.py` to change the behaviour.

 - `ROOT_URL`
     Starting/Root URL  
 - `MAX_RECURSION_LEVEL`
     Depth of traversal of the URL (10 by default, 0 means only the given domain is parsed)
 - `ONLY_SAME_DOMAIN`
     True(By default) if all the image url will be from same domain as that of entered URL  
     False if all the links will be incuded irrespective of the domain

Stores all results in the folder `files`.

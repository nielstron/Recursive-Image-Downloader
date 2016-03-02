# Recursive-Image-Downloader
It download all images from a single URL Or recursively download all images from all links in the URL

This program download all the images from a single link (level =0)
OR
It can download images from all url present in the link depending on the (level > 0)

FUNCTION NAME:
DownloadImages

Parameters:
folderpath - This takes the Download Location (BY DEFAULT, TAKES THE SCRIPT LOCATION 
url - Starting/Root URL
level - Depth of traversal of the URL (BY DEFAULT, LEVEL = 0 For The Root
FromSameDomain - True(By default) if all the image url will be from same domain as that of entered URL
                 False if all the links will be incuded irrespective of the domain

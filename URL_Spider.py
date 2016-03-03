# imageDownloader.py
# Finds and downloads all images from any given URL recursively.
# FB - 201009083
import urllib2
import re
import os
from os.path import basename
from urlparse import urlsplit

global urlList
urlList = []

# recursively download images starting from the root URL
def DownloadImages(folderpath,url, level=0,FromSameDomain=True): # the root URL is level 0
	print "Downloading From : %s" % (url)
	global urlList
	parts = url.split('//', 1)
	domainName = parts[0]+'//'+parts[1].split('/', 1)[0]
	if url in urlList: # prevent using the same URL again
		return
	urlList.append(url)
	if FromSameDomain:
		for url in urlList[:]:
			if not url.startswith(domainName):
				urlList.remove(url)
	try:
		urlContent = urllib2.urlopen(url).read()
	except:
		return
	title = str(urlContent).split('<title>')[1].split('</title>')[0]
	#folderpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),str(urlContent).split('<title>')[1].split('</title>')[0])
	print("Creating Directory : %s\n"% (title))
	os.mkdir(os.path.join(folderpath,title))
	#find and download all images
	imgUrls = re.findall('<img .*?src="(.*?)"', urlContent)
	for imgUrl in imgUrls:
		try:
			imgData = urllib2.urlopen(imgUrl).read()
			finalpath = os.path.join(folderpath,title)
			fileName = basename(urlsplit(imgUrl)[2])
			if not os.path.isfile(os.path.join(finalpath,fileName)):
				print "Downloading Image : %s"%(imgUrl)
				output = open(os.path.join(finalpath,fileName),"wb")
				output.write(imgData)
				output.close()
				print "File saved in : %s\n"%(os.path.join(finalpath,fileName))
			else:
				print "IMAGE ALREADY EXISTS... Skipping..."
		except:
			pass

	# if there are links on the webpage then recursively repeat
	if level > 0:
		linkUrls = re.findall('<a .*?href="(.*?)"', urlContent)
		if len(linkUrls) > 0:
			for linkUrl in linkUrls:
				downloadImages(os.path.join(folderpath,title),linkUrl, level - 1)

# main
url = 'http://www.google.co.in/'
startpath = os.path.dirname(os.path.abspath(__file__))

DownloadImages(startpath,url, 40)

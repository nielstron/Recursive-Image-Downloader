# imageDownloader.py
# Finds and downloads all images from any given URL recursively.
import os
from os.path import basename
from urllib import request as urllib2
from urllib.parse import urlsplit
from html.parser import HTMLParser

# Touch variable name below here

# As explained in Readme
rootUrl = "http://www.google.co.in"
onlySameDomain = True
maxRecursionLevel = 10

# Characters to be kept when creating filenames (avoiding issues in Windows based OSs)
keepcharacters = (' ', '.', '_', "-")

# don't touch anything below here

urlList = set()

# as taken from https://stackoverflow.com/a/7406369
def clean(filename):
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

def anchor(url, domainBase):
    # TODO handle case of relative path
    if url.startswith("/"):
        return domainBase + url
    return url

def fixtag(tagmatch: str):
    """ Reduces a string to the first occurence of a quote (fixes greedy regex) """
    if "\"" in tagmatch:
        return tagmatch[:tagmatch.index("\"")]
    return tagmatch

class ImageExtractHTMLParser(HTMLParser):
    title = None
    imgUrls = []
    nextUrls = []
    _title_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._title_tag = True
        if tag == "img":
            for attrk, attrv in attrs:
                if attrk == "src":
                    self.imgUrls.append(attrv)
        if tag == "a":
            for attrk, attrv in attrs:
                if attrk == "href":
                    self.nextUrls.append(attrv)

    def handle_endtag(self, tag):
        if tag == "title":
            self._title_tag = False

    def handle_data(self, data):
        if self._title_tag:
            self.title = data

# recursively download images starting from the root URL
def downloadImages(
    folderpath, url, level=0, FromSameDomain=True
):  # the root URL is level 0
    global urlList
    if url in urlList:  # prevent using the same URL again
        return
    print(f"Downloading From : {url}")
    parts = url.split("//", 1)
    domainName = parts[0] + "//" + parts[1].split("/", 1)[0]
    if FromSameDomain and not url.startswith(rootUrl):
        print("Different domain, skipping")
        return
    urlList.add(url)
    try:
        urlContentRaw = urllib2.urlopen(url).read().decode("utf8", errors="ignore")
    except Exception as e:
        print(f"Error: could not read {url}: {e}")
        return
    urlContent = ImageExtractHTMLParser()
    urlContent.feed(urlContentRaw)
    title = clean(urlContent.title)
    # folderpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),str(urlContent).split('<title>')[1].split('</title>')[0])
    print(f"Creating Directory : {title}")
    try:
        os.mkdir(os.path.join(folderpath, title))
    except FileExistsError:
        pass
    # find and download all images
    for imgUrl in urlContent.imgUrls:
        try:
            imgData = urllib2.urlopen(anchor(imgUrl, domainName)).read()
            fileName = clean(basename(urlsplit(imgUrl)[2]))
            finalpath = os.path.join(folderpath, title, fileName)
            if not os.path.isfile(finalpath):
                print(f"Downloading Image : {imgUrl} to {finalpath}")
                with open(finalpath, "wb") as output:
                    output.write(imgData)
                print(f"File saved in : {finalpath}")
            else:
                print("Image already exists... Skipping...")
        except Exception as e:
            print(f"Error: could not read {imgUrl}: {e}")

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkUrls = urlContent.nextUrls
        for linkUrl in linkUrls:
            downloadImages(os.path.join(folderpath, title), anchor(linkUrl, domainName), level - 1)


# main
if __name__ == '__main__':
    startpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    try:
        os.mkdir(startpath)
    except FileExistsError:
        pass

    downloadImages(startpath, rootUrl, 10, onlySameDomain)

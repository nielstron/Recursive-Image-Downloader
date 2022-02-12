#! /usr/env/python
# Finds and downloads all images from any given URL recursively.
import os
from os.path import basename
from urllib import request as urllib2
from urllib.parse import urlsplit
from html.parser import HTMLParser

# Touch variable name below here

# As explained in Readme
ROOT_URL = "http://www.google.co.in"
ONLY_SAME_DOMAIN = True
MAX_RECURSION_LEVEL = 10

# Characters to be kept when creating filenames (avoiding issues in Windows based OSs)
keepcharacters = (" ", ".", "_", "-")

# don't touch anything below here

URL_LIST = set()

# as taken from https://stackoverflow.com/a/7406369
def clean(filename):
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


def anchor(url, domainBase):
    # TODO handle case of relative path
    if url.startswith("/"):
        return domainBase + url
    return url


def fixtag(tagmatch: str):
    """Reduces a string to the first occurence of a quote (fixes greedy regex)"""
    if '"' in tagmatch:
        return tagmatch[: tagmatch.index('"')]
    return tagmatch


class ImageExtractHTMLParser(HTMLParser):
    title = None
    img_urls = []
    next_urls = []
    _title_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._title_tag = True
        if tag == "img":
            for attrk, attrv in attrs:
                if attrk == "src":
                    self.img_urls.append(attrv)
        if tag == "a":
            for attrk, attrv in attrs:
                if attrk == "href":
                    self.next_urls.append(attrv)

    def handle_endtag(self, tag):
        if tag == "title":
            self._title_tag = False

    def handle_data(self, data):
        if self._title_tag:
            self.title = data


# recursively download images starting from the root URL
def download(
    folderpath, url, level=0, same_domain=True
):  # the root URL is level 0
    global URL_LIST
    if url in URL_LIST:  # prevent using the same URL again
        return
    print(f"Downloading From : {url}")
    parts = url.split("//", 1)
    domain_name = parts[0] + "//" + parts[1].split("/", 1)[0]
    if same_domain and not url.startswith(ROOT_URL):
        print("Different domain, skipping")
        return
    URL_LIST.add(url)
    try:
        url_content_raw = urllib2.urlopen(url).read().decode("utf8", errors="ignore")
    except Exception as e:
        print(f"Error: could not read {url}: {e}")
        return
    url_content = ImageExtractHTMLParser()
    url_content.feed(url_content_raw)
    title = clean(url_content.title)
    print(f"Creating Directory : {title}")
    try:
        os.mkdir(os.path.join(folderpath, title))
    except FileExistsError:
        pass
    # find and download all images
    for img_url in url_content.img_urls:
        try:
            img_url = anchor(img_url, domain_name)
            img_data = urllib2.urlopen(img_url).read()
            file_name = clean(basename(urlsplit(img_url)[2]))
            final_path = os.path.join(folderpath, title, file_name)
            if not os.path.isfile(final_path):
                print(f"Downloading Image : {img_url} to {final_path}")
                with open(final_path, "wb") as output:
                    output.write(img_data)
                print(f"File saved in : {final_path}")
            else:
                print("Image already exists... Skipping...")
        except Exception as e:
            print(f"Error: could not read {img_url}: {e}")

    # if there are links on the webpage then recursively repeat
    if level > 0:
        link_urls = url_content.next_urls
        for link_url in link_urls:
            download(
                os.path.join(folderpath, title), anchor(link_url, domain_name), level - 1
            )


# main
if __name__ == "__main__":
    startpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    try:
        os.mkdir(startpath)
    except FileExistsError:
        pass

    download(startpath, ROOT_URL, MAX_RECURSION_LEVEL, ONLY_SAME_DOMAIN)

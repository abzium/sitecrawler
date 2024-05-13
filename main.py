# This program generates something similar to a sitemap
# The problem I have with sitemap generators is this:
# If an unwanted link shows up, I don't have any way of knowing from which page the link was accessed from
# I aim to solve that by including which pages link to each page in the sitemap

import requests
import re

url_to_search = "http://cflit3.vmx.link"
# remove the slash for formatting further links
if url_to_search.endswith('/'):
    url_to_search = url_to_search[:-1]

html_pattern = re.compile(r'href="/[\S]*html"')
slash_pattern = re.compile(r'href="/[\S]*/"')

r = requests.get(url_to_search)

# print(r.text)
htmls = html_pattern.findall(r.text)
slashes = slash_pattern.findall(r.text)

urls = list(set(htmls + slashes))
urls.sort()

# make each url into a proper link
for i in range(len(urls)):
    urls[i] = urls[i].replace('href="', url_to_search)
    urls[i] = urls[i].replace('"', '')

for i in urls:
    print(i)

print("All done!")

# href="/Internet/"
# <a class="btn-style-two theme-btn btn-item" href="/Internet/">
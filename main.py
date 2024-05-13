# This program generates something similar to a sitemap
# The problem I have with sitemap generators is this:
# If an unwanted link shows up, I don't have any way of knowing from which page the link was accessed from
# I aim to solve that by including which pages link to each page in the sitemap

import requests
import re
from collections import deque

def get_links_from_url(url_to_search, base_url) -> 'list':
    # visits a link and returns a list of all discovered links
    if url_to_search.endswith('/'):
        url_to_search = url_to_search[:-1]

    r = requests.get(url_to_search)

    html_pattern = re.compile(r'href="/[\S]*html"')
    slash_pattern = re.compile(r'href="/[\S]*/"')

    htmls = html_pattern.findall(r.text)
    slashes = slash_pattern.findall(r.text)

    urls = list(set(htmls + slashes))

    for i in range(len(urls)):
        urls[i] = urls[i].replace('href="', base_url)
        urls[i] = urls[i].replace('"', '')

    return urls
    

base_url = "https://www.sineris.com"

visited = deque()
queue = deque()

visited.append(base_url)
url_list = get_links_from_url(base_url, base_url)

for item in url_list:
    queue.append(item)


while queue:
    url = queue.pop()
    if url in visited:
        # print(f"{url} was already visited!")
        continue
    else:
        # print(f"{url} is now being visited...")
        visited.append(url)
        url_list = get_links_from_url(url, base_url)
        for item in url_list:
            queue.append(item)

print("============ RESULTS ============")
for i in visited:
    print(i)

# href="/Internet/"
# <a class="btn-style-two theme-btn btn-item" href="/Internet/">
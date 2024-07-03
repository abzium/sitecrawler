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
    

base_url = input("Enter base url (ex. https://www.example.com): ")

visited = {}
queue = deque()

visited[base_url] = []
url_list = get_links_from_url(base_url, base_url)

for item in url_list:
    queue.append((item, base_url))

while queue:
    url = queue.pop()
    if url[0] in visited.keys():
        # Update the information on the visited dict
        visited[url[0]].append(url[1])
    else:
        print(f"{url[0]} is now being visited...")
        # visited.append(url)
        visited[url[0]] = [url[1]]
        url_list = get_links_from_url(url[0], base_url)
        for item in url_list:
            queue.append((item, url[0]))

print("============ RESULTS ============")
for i in visited.keys():
    print(i)
    print(visited[i])
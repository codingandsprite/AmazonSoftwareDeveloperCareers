from collections import namedtuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup

POSTS = dict()

Post = namedtuple('Post', ['link', 'title', 'date'])

LAST_PAGE = 10

url = "https://careers.walmart.com/api/search?q=&page={page}&sort=rank&jobCategory=00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bfd-da32-a37b-fbff3a4a0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000018b-4920-d494-a3cb-edb3f3c30000,0000018b-4926-dbdf-a19b-6fbe42760000,0000018b-4930-de4a-ad9f-59ff51360000,0000018b-48a1-de4a-ad9f-58ff99ef0000,0000017c-a4f6-dfa9-a77d-acf64f2f0000,0000018b-4919-d494-a3cb-ed9be5390000,0000018b-4926-da98-adfb-79e7eca60000,0000018b-492b-de4a-ad9f-59ffa0d10000,0000018b-492d-dbdf-a19b-6fbffa350000,0000018b-492d-de4a-ad9f-59ff17530000,0000018b-492c-d283-abeb-5b7c8e360000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bfd-da32-a37b-fbff3a4a0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://careers.walmart.com/api/search?q=&page=1&sort=rank&jobCategory=00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bfd-da32-a37b-fbff3a4a0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000018b-4920-d494-a3cb-edb3f3c30000,0000018b-4926-dbdf-a19b-6fbe42760000,0000018b-4930-de4a-ad9f-59ff51360000,0000018b-48a1-de4a-ad9f-58ff99ef0000,0000017c-a4f6-dfa9-a77d-acf64f2f0000,0000018b-4919-d494-a3cb-ed9be5390000,0000018b-4926-da98-adfb-79e7eca60000,0000018b-492b-de4a-ad9f-59ffa0d10000,0000018b-492d-dbdf-a19b-6fbffa350000,0000018b-492d-de4a-ad9f-59ff17530000,0000018b-492c-d283-abeb-5b7c8e360000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bfd-da32-a37b-fbff3a4a0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "TE": "trailers",
}


for page in range(1, (LAST_PAGE+1)):
    response = requests.get(
        url=url.format(page=page),
        headers=headers,
    )
    
    search_results = BeautifulSoup(response.text, "html.parser").find_all(class_="search-result")

    for search_result in search_results:
        link = search_result.find('a')['href']
        title, category, location, date_str = [x for x in search_result.stripped_strings]
        date_obj = datetime.strptime(date_str, '%m/%d/%y')
        date = date_obj.strftime("%a, %d %b %Y 12:00:00 GMT")
        POSTS[link] = Post(link, title, date)

STREAM = sorted([POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True)

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join([ r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Walmart - Technology</title>""",
            r"""<description>Walmart - Technology</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</pubDate>""",
            r"""<lastBuildDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</lastBuildDate>""",
            "\n".join([r"""<item><title><![CDATA["""+x.title+r"""]]></title><link>"""+x.link+r"""</link><pubDate>"""+x.date+r"""</pubDate></item>""" for x in STREAM]),
            r"""</channel>""",
            r"""</rss>""",
    ])

    print(XML)

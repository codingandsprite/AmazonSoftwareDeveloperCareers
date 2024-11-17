from collections import namedtuple
from datetime import datetime
import requests

POSTS = dict()

Post = namedtuple("Post", ["link", "title", "date"])

url = "https://www.amazon.jobs/api/jobs/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.amazon.jobs/content/en/job-categories/software-development?country^%^5B^%^5D=US",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://www.amazon.jobs",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
}

json_data = {
    "accessLevel": "EXTERNAL",
    "contentFilterFacets": [
        {"name": "primarySearchLabel", "requestedFacetCount": 9999}
    ],
    "excludeFacets": [
        {"name": "isConfidential", "values": [{"name": "1"}]},
        {"name": "businessCategory", "values": [{"name": "a-confidential-job"}]},
    ],
    "filterFacets": [
        {
            "name": "category",
            "requestedFacetCount": 9999,
            "values": [{"name": "Software Development"}],
        }
    ],
    "includeFacets": [],
    "jobTypeFacets": [],
    "locationFacets": [
        [
            {
                "name": "country",
                "requestedFacetCount": 9999,
                "values": [{"name": "US"}],
            },
            {"name": "normalizedStateName", "requestedFacetCount": 9999},
            {"name": "normalizedCityName", "requestedFacetCount": 9999},
        ]
    ],
    "query": "",
    "size": 100,
    "start": 0,
    "treatment": "OM",
    "sort": {"sortOrder": "DESCENDING", "sortType": "CREATED_DATE"},
}

response = requests.post(
    url=url,
    headers=headers,
    json=json_data,
)

jobs = dict(response.json())['searchHits']
for job in jobs:
    is_intern = job['fields']['isIntern'][0]
    is_manager = job['fields']['isManager'][0]
    preferred_qualifications = job['fields']['preferredQualifications'][0]
    company_name = job['fields']['companyName'][0]
    description = job['fields']['description'][0]
    title = job['fields']['title'][0]
    job_role = job['fields']['jobRole'][0]
    id = job['fields']['urlNextStep'][0].split("/")[-2]
    link = "https://amazon.jobs/en/jobs/"+id+"/"
    date = job['fields']['updatedDate'][0]
    full_title = f"{job_role} @ {company_name}"
    if not (link in POSTS.keys()):
        POSTS[link] = Post(link, full_title, date)

STREAM = sorted(
    [POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True
)

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join(
        [
            r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Amazon Software Developer Roles</title>""",
            r"""<description>Amazon Software Developer Roles</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</pubDate>""",
            r"""<lastBuildDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</lastBuildDate>""",
            "\n".join(
                [
                    r"""<item><title><![CDATA["""
                    + x.title
                    + r"""]]></title><link>"""
                    + x.link
                    + r"""</link><pubDate>"""
                    + datetime.utcfromtimestamp(int(x.date)).strftime('%a, %d %b %Y %H:%M:%S GMT')
                    + r"""</pubDate></item>"""
                    for x in STREAM
                ]
            ),
            r"""</channel>""",
            r"""</rss>""",
        ]
    )

    print(XML)

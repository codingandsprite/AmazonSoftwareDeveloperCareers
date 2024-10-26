from collections import namedtuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup

POSTS = dict()

Post = namedtuple("Post", ["link", "title", "date"])

url = "https://www.amazon.jobs/api/jobs/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.amazon.jobs/content/en/job-categories/software-development?country^%^5B^%^5D=US",
    # "x-api-key": "PbxxNwIlTi4FP5oijKdtk3IrBF5CLd4R4oPHsKNh",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://www.amazon.jobs",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    # "Cookie": "check_for_eu_countries=false; amazon_jobs_session=b04yTFFkN0ZQN3p6NXZ5UlNIMjBOMUE3SjlrVE1yU09BWHVqd2wwTzhYOVNjNzZmd0ZCZmU3YWVZVTRhMTFYK29FMlZuZ0JKOHZLODkvSnMwbGJsWllLNk9MTFFFTzdsNW9hcFJMZVdXclp1cG11bHM2dHBGdjFra2hVV0lHeTNjbFB4M0M4TUZJTWlBSDNDNFd0ejhjWGpNUEFJdElRWVdnbDZsODdnMjdzMXpwUy9xUUs0dzV5L2d4ekFRQTRWOURzRnFRalRyUFBwS2FsLzVVOFlKYjh0WDdtaXFEbTVXRVcwOVowVTdrMEdtcmpjdUlYZFhoOXJXZy84bWlRSEpzYjlGbHVUV202RmRNRFNHL0djM3RUSnNMZFN4NUFBamRaOU45aVNBMnNxeFJocXlQY3B6QnliTHc3UTh5aWY2OEtXcjR6MGxmSDZSc3p3bzhPTHhFTkQzbmZnaEVrREJMbXlmTzVCM0YwPS0tR1JsNFZKSFlvaDVUMkRlMnpDQXQzZz09--52608192b145242db6350307bf4167c1eb2e86b4; AMCV_CCBC879D5572070E7F000101^%^40AdobeOrg=-1124106680^%^7CMCIDTS^%^7C20023^%^7CMCMID^%^7C64714743694667807955257447786543762494^%^7CMCAID^%^7CNONE^%^7CMCOPTOUT-1729980581s^%^7CNONE^%^7CvVersion^%^7C5.2.0; AMCVS_CCBC879D5572070E7F000101^%^40AdobeOrg=1; cookie_preferences=^%^7B^%^22advertising^%^22^%^3Atrue^%^2C^%^22analytics^%^22^%^3Atrue^%^2C^%^22version^%^22^%^3A2^%^7D; analytics_id=79b0ec6b-f77f-4941-924d-1e9cb7b8ed28; __Host-mons-sid=135-3934453-6531100; advertising_id=2c52e139-a2cf-4067-aaaa-dc2c4eb5a166; source=^%^7B^%^22azref^%^22^%^3A^%^22https^%^3A^%^2F^%^2Faccount.amazon.jobs^%^2F^%^22^%^7D; __Host-mons-ubid=134-5202813-9131817; cwr_u=c01f2ee8-1858-4f91-9af1-750e1f828b0c; _ga=GA1.2.1734377627.1729967497; csm-sid=058-3320574-2292749; __Host-mons-st=LsAvDRqkhmDw1WvvMGUC1/45HBaG5gBKW/nPd4amBFbRs4M6ScBhRmu/yWDEJI5wJg697L5NxWut8ZcvB8PdJ+EC0DHhZ9AsS5r445EKF6ycGpTW01NM24tfrpbhhAT9C91OdEplneorv+x6hd8/bfqc5Jo7UjBatIWjfWp338d0xa2H5stsowNyXDW2T5vMAzuH0PrWg3CoXHZOCBedzp4d8YB2kQhy8OYJZJE3wsfdnQ4gYm/Cy/bL3UJxi+cFaeRt4U+2IKC1Fvu1nlIFFpkeaAYoTOGg925DmAlKCL9O/jpXFAOooTr9lgqX0+KrFDpnv83MrlwWH5MfYw9eSzYsxumUwwms; geolocation=US; preferred_locale=en-US; _gat=1; cwr_s_bedc9b2b-623c-479f-9141-5aac958fce05=eyJzZXNzaW9uSWQiOiIxZTMyZjJkZC1lMTQ4LTRjMWItYTljMS0yMjQ0YWJkMzM2MjkiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjI3MSwicGFnZSI6eyJwYWdlSWQiOiIvY29udGVudC9lbi9qb2ItY2F0ZWdvcmllcy9zb2Z0d2FyZS1kZXZlbG9wbWVudCIsInBhcmVudFBhZ2VJZCI6Ii9jb250ZW50L2VuL2NhcmVlci1wcm9ncmFtcy91bml2ZXJzaXR5IiwiaW50ZXJhY3Rpb24iOjMsInJlZmVycmVyIjoiaHR0cHM6Ly93d3cuYW1hem9uLmpvYnMvZW4iLCJyZWZlcnJlckRvbWFpbiI6Ind3dy5hbWF6b24uam9icyIsInN0YXJ0IjoxNzI5OTczMzM4MDQ5fX0=; cwr_s_a727750b-28d3-4e1d-81fe-8eece247d35b=eyJzZXNzaW9uSWQiOiI3MjA2Y2UxNy03OWU4LTRiZDAtOTFlMy1mZGE3ZGFjNDViNTYiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjUyLCJwYWdlIjp7InBhZ2VJZCI6Ii9lbi9qb2JzLzI3OTI2NDYvc29mdHdhcmUtZGV2ZWxvcG1lbnQtZW5naW5lZXItaWktcmlzYy1maXhlZC1qdWxpZS16aGFuZyIsInBhcmVudFBhZ2VJZCI6Ii9lbiIsImludGVyYWN0aW9uIjo2LCJyZWZlcnJlciI6IiIsInJlZmVycmVyRG9tYWluIjoiIiwic3RhcnQiOjE3Mjk5NzMzODEyMjF9fQ==",
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
    #"cookieInfo": "check_for_eu_countries=false;AMCV_CCBC879D5572070E7F000101%40AdobeOrg=-1124106680%7CMCIDTS%7C20023%7CMCMID%7C64714743694667807955257447786543762494%7CMCAID%7CNONE%7CMCOPTOUT-1729980581s%7CNONE%7CvVersion%7C5.2.0; AMCVS_CCBC879D5572070E7F000101%40AdobeOrg=1; cookie_preferences=%7B%22advertising%22%3Atrue%2C%22analytics%22%3Atrue%2C%22version%22%3A2%7D; analytics_id=79b0ec6b-f77f-4941-924d-1e9cb7b8ed28; __Host-mons-sid=135-3934453-6531100; advertising_id=2c52e139-a2cf-4067-aaaa-dc2c4eb5a166; source=%7B%22azref%22%3A%22https%3A%2F%2Faccount.amazon.jobs%2F%22%7D; __Host-mons-ubid=134-5202813-9131817; _ga=GA1.2.1734377627.1729967497; csm-sid=058-3320574-2292749; __Host-mons-st=LsAvDRqkhmDw1WvvMGUC1/45HBaG5gBKW/nPd4amBFbRs4M6ScBhRmu/yWDEJI5wJg697L5NxWut8ZcvB8PdJ+EC0DHhZ9AsS5r445EKF6ycGpTW01NM24tfrpbhhAT9C91OdEplneorv+x6hd8/bfqc5Jo7UjBatIWjfWp338d0xa2H5stsowNyXDW2T5vMAzuH0PrWg3CoXHZOCBedzp4d8YB2kQhy8OYJZJE3wsfdnQ4gYm/Cy/bL3UJxi+cFaeRt4U+2IKC1Fvu1nlIFFpkeaAYoTOGg925DmAlKCL9O/jpXFAOooTr9lgqX0+KrFDpnv83MrlwWH5MfYw9eSzYsxumUwwms; geolocation=US; preferred_locale=en-US; _gat=1; cwr_s_a727750b-28d3-4e1d-81fe-8eece247d35b=eyJzZXNzaW9uSWQiOiI3MjA2Y2UxNy03OWU4LTRiZDAtOTFlMy1mZGE3ZGFjNDViNTYiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjUyLCJwYWdlIjp7InBhZ2VJZCI6Ii9lbi9qb2JzLzI3OTI2NDYvc29mdHdhcmUtZGV2ZWxvcG1lbnQtZW5naW5lZXItaWktcmlzYy1maXhlZC1qdWxpZS16aGFuZyIsInBhcmVudFBhZ2VJZCI6Ii9lbiIsImludGVyYWN0aW9uIjo2LCJyZWZlcnJlciI6IiIsInJlZmVycmVyRG9tYWluIjoiIiwic3RhcnQiOjE3Mjk5NzMzODEyMjF9fQ==; cwr_u=c01f2ee8-1858-4f91-9af1-750e1f828b0c; cwr_s_bedc9b2b-623c-479f-9141-5aac958fce05=eyJzZXNzaW9uSWQiOiIxZTMyZjJkZC1lMTQ4LTRjMWItYTljMS0yMjQ0YWJkMzM2MjkiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjI3MSwicGFnZSI6eyJwYWdlSWQiOiIvY29udGVudC9lbi9qb2ItY2F0ZWdvcmllcy9zb2Z0d2FyZS1kZXZlbG9wbWVudCIsInBhcmVudFBhZ2VJZCI6Ii9jb250ZW50L2VuL2NhcmVlci1wcm9ncmFtcy91bml2ZXJzaXR5IiwiaW50ZXJhY3Rpb24iOjMsInJlZmVycmVyIjoiaHR0cHM6Ly93d3cuYW1hem9uLmpvYnMvZW4iLCJyZWZlcnJlckRvbWFpbiI6Ind3dy5hbWF6b24uam9icyIsInN0YXJ0IjoxNzI5OTczMzM4MDQ5fX0=",
    "sort": {"sortOrder": "DESCENDING", "sortType": "CREATED_DATE"},
}

response = requests.post(
    url=url,
    headers=headers,
    json=json_data,
)

jobs = dict(response.json())['searchHits']

for job in jobs:
    title = job['fields']['title'][0]
    role = job['fields']['jobRole'][0]
    id = job['fields']['urlNextStep'][0].split("/")[-2]
    link = "https://amazon.jobs/en/jobs/"+id+"/"
    date = job['fields']['updatedDate'][0]
    POSTS[link] = Post(link, title, date)

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
            r"""<title>Walmart - Technology</title>""",
            r"""<description>Walmart - Technology</description>""",
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
                    + x.date
                    + r"""</pubDate></item>"""
                    for x in STREAM
                ]
            ),
            r"""</channel>""",
            r"""</rss>""",
        ]
    )

    print(XML)

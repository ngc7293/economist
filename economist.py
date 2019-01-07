#!/usr/bin/env python3
"""Download and transform into markdown articles from the Economist."""

import argparse
import datetime

import requests
import bs4

keep_tags = [
    'small'
]


def sanitize(paragraph):
    paragraph = paragraph.decode_contents()

    start = 0
    i = 0
    while i < len(paragraph):
        char = paragraph[i]

        if char == '<':
            start = i

        elif char == '>':
            tag = paragraph[start:i]
            if tag[1:] not in keep_tags and tag[2:] not in keep_tags:
                paragraph = paragraph[0:start] + paragraph[i + 1:]
                i = start
        i += 1
    return paragraph

try:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--ext', required=True, choices=['.html', '.md'])
    args = parser.parse_args()

    response = requests.get(args.url)
    soup = bs4.BeautifulSoup(response.text, features="lxml")

    content = soup.select('.main-content__clearfix')[0]

    title = content.select('.flytitle-and-title__title')[0].extract().string
    subtitle = content.select('.blog-post__rubric')[0].extract().string
    image = content.select('.blog-post__image')[0].img.extract()
    postdate = datetime.datetime.strptime(content.select('time.blog-post__datetime')[0].extract()['datetime'], '%Y-%m-%dT%H:%M:%SZ')

    content = content.select('.blog-post__text')[0].extract()
    paragraphs = [sanitize(tag) for tag in content.contents if tag.name == 'p']
    paragraphs = [p for p in paragraphs if p]  # remove empty paragraphs


    with open("economist" + args.ext, 'r') as file:
        template = file.read()

    with open(args.url.split('/')[-1] + args.ext, 'w') as file:
        file.write(template.format(**{
            'title': title,
            'subtitle': subtitle,
            'image': {
                'source': image['src'],
                'alt': image['alt']
            },
            'content': ''.join(['<p>' + p + '</p>' for p in paragraphs]),

            'postdate': postdate.strftime("%Y-%m-%d at %H:%M:%SZ"),
            'getdate': datetime.datetime.utcnow().strftime("%Y-%m-%d at %H:%M:%SZ"),
            'url': args.url
        }))

except:
    print('\033[31m', end='')

print('[{postdate}] {title}\033[0m'.format(**{
        'title': title, 
        'postdate': postdate}
    ))
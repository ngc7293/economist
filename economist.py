#!/usr/bin/env python3
"""Download and transform into markdown articles from the Economist."""

import argparse
import datetime

import requests
import jinja2
import bs4

keep_tags = [
    'small',
    'strong',
    'em'
]

def sanitize(paragraph):
    toptag = paragraph.name
    paragraph = paragraph.decode_contents()

    out = {
        'text': '',
        'rich': ''
    }
    start = -1
    i = 0
    while i < len(paragraph):
        char = paragraph[i]

        if char == '<':
            start = i

        elif char == '>':
            tag = paragraph[start:i]
            if tag[1:] in keep_tags or tag[2:] in keep_tags:
                out['rich'] += paragraph[start:i + 1]
            start = -1

        elif start == -1:
            out['text'] += char
            out['rich'] += char

        i += 1
    out['rich'] = '<{tag}>{content}</{tag}>'.format(tag=toptag, content=out['rich']) 
    if out['text'] == '':
        return {}
    return out

def convert(url, ext, flask=False):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features="lxml")

    content = soup.select('.main-content__clearfix')[0]

    title = content.select('.flytitle-and-title__title')[0].extract().string
    subtitle = content.select('.blog-post__description')[0].extract().string
    image = content.select('.blog-post__image')[0].img.extract()
    postdate = datetime.datetime.strptime(content.select('time.blog-post__datetime')[0].extract()['datetime'], '%Y-%m-%dT%H:%M:%SZ')

    content = content.select('.blog-post__text')[0].extract()
    paragraphs = [sanitize(tag) for tag in content.contents if tag.name in ['p', 'h2']]
    paragraphs = [p for p in paragraphs if p]  # remove empty paragraphs

    if ext == '.html':
        paragraphs[-1]['text'] = paragraphs[-1]['text'].replace('■', '')
        paragraphs[-1]['rich'] = paragraphs[-1]['rich'].replace('■', '')

    with open("templates/economist" + ext, 'r') as file:
        template = jinja2.Template(file.read())

    with open('articles/' + url.split('/')[-1] + ext, 'w') as file:
        file.write(template.render({
            'title': title,
            'subtitle': subtitle,
            'image': {
                'source': image['src'],
                'alt': image['alt']
            },
            'content': paragraphs,

            'postdate': postdate.strftime("%Y-%m-%d at %H:%M:%SZ"),
            'getdate': datetime.datetime.utcnow().strftime("%Y-%m-%d at %H:%M:%SZ"),
            'url': url,
            'flask': flask
        }))

    print('[{postdate}] {title}\033[0m'.format(**{
            'title': title, 
            'postdate': postdate}
        ))

    return 'articles/' + url.split('/')[-1] + ext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--ext', required=True, choices=['.html', '.md', '.reddit.md'])
    args = parser.parse_args()
    convert(args.url, args.ext)
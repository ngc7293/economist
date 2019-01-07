# economist

Download articles from The Economist's website and export them to a minimal HTML or Markdown file. Why? The Economist's website looks nice, but is extremely bloated. With this script, a 700k characters HTML page is reduced to a measly 7k.

It currently contains three templates:

- `.html`, a simple html structure which, if displayed with the accompanying CSS, emulates the print edition look
- `.md`, a simple common markdown output
- `.reddit.md`, made to look nice in Reddit comments

## Dependencies

- Python 3
- BeautifulSoup 4
- Requests
- Jinja2

## TODO:

- Download images (it currently hotlinks)
- Download in-line pictures and graphs
- Support more output formats
- Automatically download new articles (from RSS)
- ~~Infrige more copyright~~
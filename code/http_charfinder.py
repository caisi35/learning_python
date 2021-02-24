import sys
import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

TEMPLATE_NAME = 'http_charfinder.html'
CONTENT_TYPE = 'text/html; charset=UTF-8'
SAMPLE_WORDS = ('bismillah chess cat ciecled Malayalam digit Roman face Ethiopic black mark symbol dot operator Braille hexagram').split()

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in sorted(SAMPLE_WORDS, key=str.upper))

index = UnicodeNameIndex()
with open(TEMPLATE_NAME) as tpl:
    template = tpl.read()
    
template = template.replace('{links}', LINKS_HTML)

def home(request):
    print(dir(request), ':', request.query)
    query = request.GET.get('query', '').strip()
    print('Query: {!r}'.format(query))
    if query:
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**vars(descr)) for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'
    
    html = template.format(query=query, result=res, message=msg)
    print('Senting {} results'.format(len(descriptions)))
    return web.Response(content_type=CONTENT_TYPE, text=html)
  

@asyncio.coroutine
def init(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', home)
    handler = app.make_handler()
    server = yield from loop.create_server(handler, address, port)
    return server.sockets[0].getsockname()


def main(address='127.0.0.1', port=8889):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))
    print('Serveing on {}. Hit CTRL-C stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print('Server shutting down.')
    loop.close()
    

if __name__ == '__main__':
    main(*sys.argv[1:])
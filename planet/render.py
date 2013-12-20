import logging
import os
import time

from . import htmltmpl
from .constants import __url__, TIMEFMT_ISO, TIMEFMT_822, VERSION


log = logging.getLogger(__name__)


def render_template(
        template_file,
        planet_name,
        planet_link,
        planet_feed,
        owner_name,
        owner_email,
        output_dir,
        date_format,
        encoding,
        channels_list,
        items_list):
    log.info("Processing template %s", template_file)
    
    # We treat each template individually
    base = os.path.splitext(os.path.basename(template_file))[0]
    url = os.path.join(planet_link, base)
    output_file = os.path.join(output_dir, base)
    
    date = time.gmtime()
    kwargs = {
        'Items': items_list,
        'Channels': channels_list,
        'generator': VERSION,
        'name': planet_name,
        'link': planet_link,
        'owner_name': owner_name,
        'owner_email': owner_email,
        'url': url,
        'repo_url': __url__,
        'date': time.strftime(date_format, date),
        'date_iso': time.strftime(TIMEFMT_ISO, date),
        'date_822': time.strftime(TIMEFMT_822, date)
    }
        
    if planet_feed:
        kwargs['feed'] = planet_feed
        kwargs['feedtype'] = planet_feed.find('rss')>=0 and 'rss' or 'atom'

    if template_file.endswith('.tmpl'):
        func = render_htmltmpl
    else:
        assert template_file.endswith('.html')
        func = render_jinja
    return func(template_file, output_file, encoding, kwargs)


def render_htmltmpl(
        template_file,
        output_file,
        encoding,
        template_kwargs):
    manager = htmltmpl.TemplateManager()
    try:
        template = manager.prepare(template_file)
    except htmltmpl.TemplateError:
        template = manager.prepare(os.path.basename(template_file))

    # Process the template
    tp = htmltmpl.TemplateProcessor(html_escape=0)
    for key, val in template_kwargs.iteritems():
        tp.set(key, val)

    log.info("Writing %s", output_file)
    with open(output_file, "w") as output_fd:
        if encoding.lower() in ("utf-8", "utf8"):
            # UTF-8 output is the default because we use that internally
            output_fd.write(tp.process(template))
        elif encoding.lower() in ("xml", "html", "sgml"):
            # Magic for Python 2.3 users
            output = tp.process(template).decode("utf-8")
            output_fd.write(output.encode("ascii", "xmlcharrefreplace"))
        else:
            # Must be a "known" encoding
            output = tp.process(template).decode("utf-8")
            output_fd.write(output.encode(encoding, "replace"))


def render_jinja(*args, **kwargs):
    raise NotImplementedError()

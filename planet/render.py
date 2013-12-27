import logging
import os
import time

import jinja2

from . import htmltmpl
from .constants import TIMEFMT_ISO, TIMEFMT_822, VERSION


log = logging.getLogger(__name__)


def render_template(
        template_file,
        output_dir,
        date_format,
        encoding,
        channels_list,
        items_list,
        planet_kwargs):
    """Render a template file.
    Chooses renderer based on template_file extension.

    :param planet_kwargs: Extra Planet-level parameters in the config.
    """
    log.info("Processing template %s", template_file)
    
    # We treat each template individually
    base = os.path.basename(template_file)
    # Templates may be '.html' or '.html.tmpl', etc.
    # Don't throw away the last extension.
    if base.count('.') > 1:
        base = os.path.splitext(base)[0]
    url = os.path.join(planet_kwargs['link'], base).replace('\\', '/')
    output_file = os.path.join(output_dir, base)
    
    date = time.gmtime()
    kwargs = dict(planet_kwargs)
    kwargs.update({
        'Items': items_list,
        'Channels': channels_list,
        'generator': VERSION,
        'url': url,
        'date': time.strftime(date_format, date),
        'date_iso': time.strftime(TIMEFMT_ISO, date),
        'date_822': time.strftime(TIMEFMT_822, date)
    })

    kwargs['feedtype'] = kwargs['feed'].find('rss')>=0 and 'rss' or 'atom'

    if template_file.endswith('.tmpl'):
        func = render_htmltmpl
    else:
        assert template_file.endswith('.html')
        func = render_jinja
    assert 'template_files'  not in kwargs
    html = func(template_file, kwargs)


    log.info("Writing %s", output_file)
    with open(output_file, "w") as output_fd:
        if encoding.lower() in ("utf-8", "utf8"):
            # UTF-8 output is the default because we use that internally
            output_fd.write(html)
        elif encoding.lower() in ("xml", "html", "sgml"):
            # Magic for Python 2.3 users
            output = html.decode("utf-8")
            output_fd.write(output.encode("ascii", "xmlcharrefreplace"))
        else:
            # Must be a "known" encoding
            output = html.decode("utf-8")
            output_fd.write(output.encode(encoding, "replace"))


def render_htmltmpl(template_file, template_kwargs):
    manager = htmltmpl.TemplateManager()
    try:
        template = manager.prepare(template_file)
    except htmltmpl.TemplateError:
        template = manager.prepare(os.path.basename(template_file))

    # Process the template
    tp = htmltmpl.TemplateProcessor(html_escape=0)
    for key, val in template_kwargs.iteritems():
        tp.set(key, val)

    return tp.process(template)


def render_jinja(template_file, template_kwargs):
    for key in 'Items', 'Channels':
        newobjs = []
        for oldobj in template_kwargs[key]:
            newobj = {}
            for k, v in oldobj.iteritems():
                if isinstance(v, str):
                    v = v.decode('utf8')
                newobj[k] = v
            newobjs.append(newobj)
        template_kwargs[key] = newobjs

    with open(template_file) as f:
        template = jinja2.Template(f.read())
    html = template.render(**template_kwargs)
    return html.encode('utf8')

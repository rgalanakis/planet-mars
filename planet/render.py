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
    manager = htmltmpl.TemplateManager()
    log.info("Processing template %s", template_file)
    try:
        template = manager.prepare(template_file)
    except htmltmpl.TemplateError:
        template = manager.prepare(os.path.basename(template_file))

    # We treat each template individually
    base = os.path.splitext(os.path.basename(template_file))[0]
    url = os.path.join(planet_link, base)
    output_file = os.path.join(output_dir, base)

    # Process the template
    tp = htmltmpl.TemplateProcessor(html_escape=0)
    tp.set("Items", items_list)
    tp.set("Channels", channels_list)

    # Generic information
    tp.set("generator", VERSION)
    tp.set("name", planet_name)
    tp.set("link", planet_link)
    tp.set("owner_name", owner_name)
    tp.set("owner_email", owner_email)
    tp.set("url", url)
    tp.set("repo_url", __url__)

    if planet_feed:
        tp.set("feed", planet_feed)
        tp.set("feedtype", planet_feed.find('rss')>=0 and 'rss' or 'atom')

    # Update time
    date = time.gmtime()
    tp.set("date", time.strftime(date_format, date))
    tp.set("date_iso", time.strftime(TIMEFMT_ISO, date))
    tp.set("date_822", time.strftime(TIMEFMT_822, date))

    try:
        log.info("Writing %s", output_file)
        output_fd = open(output_file, "w")
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
        output_fd.close()
    except KeyboardInterrupt:
        raise
    except:
        log.exception("Write of %s failed", output_file)

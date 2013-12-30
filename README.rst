Planet Mars
-----------

**Planet Mars** is a flexible feed aggregator.
It downloads news feeds published by web sites and
aggregates their content together into a single combined feed,
latest news first.

This is a fork of the Python planet feed aggregator
originally available at http://www.planetplanet.org/
The name **Planet Mars** comes from the idea that this is a ruthlessly
simple alternative to other Python-based Planet aggregators,
such as the lovely **Planet Venus** 
( http://www.intertwingly.net/code/venus/ ), 
which is much more full featured.

**Planet Mars** uses Jinja2 for its templating engine,
though htmltmpl (based on Perl's ``HTML::Template`` module)
is still supported.
If you want Django or another templating engine,
just put in a ticket, it should be pretty easy.

Installation
------------

This software is pretty simple and Python 2.6 and
later should work.

To install Planet Mars, you can just use
``pip`` or ``easy_install``.
There are a few dependencies that should be installed automatically.

You can then use it like a normal Python package.

Usage
-----

Generally usage is split into two parts:
setup and generation.
Setup is only done when setting up your site,
and generation is done on some schedule.

Setup
=====

1. Copy the ``planet/example`` folder and paste it
   where you want to keep the file generator and your custom files.
2. Edit ``config.ini``. The file is heavily commented and
   should guide you through how to customize it.
3. Create your template files for your HTML page or pages
   (or edit ``index.html``).
   The feed templates are provided by Planet,
   you just need to provide your html templates.
4. Create the supporting files your html page links to,
   like images and CSS, and put them into your output folder.
   Or just edit the ones that are already there.
3. Point to your template file(s) from your ``.ini`` file
   (skip this step if you just edited ``index.html``).
4. You're done!
   If you wish to back up your customization
   (storing your config and templates in version control),
   I'd suggest following the example of ``planet-techart``:
   https://github.com/techartorg/planet-techart

Generation
==========

Create some script to call
``python -m planet <your folder>/config.ini``
on a schedule.
Then copy over ``<your folder>/output``
(or whatever output you specified in config.ini)
to wherever you want to serve files from.

Template files
==============

The template files used are given as a space separated list in the
'template_files' option in config.ini. Their extension determines which
rendering engine they use ('.html', '.tmpl') and the rest of their name
determines their path in the output directory.

The options under the ``[Planet]`` section of the config 
are available to the template.

There are also two loops, 'Items' and 'Channels'.  All of the lines of
the template and variable substitutions are available for each item or
channel.

Channels loop
+++++++++++++

The 'Channels' loop iterates all of the channels (feeds) defined in the
configuration file, within it the following variables are available:

* name: value of the 'name' option in config.ini, or title
* title: title retreived from the channel's feed
* tagline: description retreived from the channel's feed
* link: link for the human-readable content (from the feed)
* url: url of the channel's feed itself

Additionally the value of any other option specified in config.ini
for the feed, or in the ``[DEFAULT]`` section, is available as a
variable of the same name.

Depending on the feed, there may be a huge variety of other
variables may be available.

Items loop
++++++++++

The 'Items' loop iterates all of the blog entries from all of the channels,
you do not place it inside a 'Channels' loop.  Within it, the following
variables are available:

* id: unique id for this entry (sometimes just the link)
* link: link to a human-readable version at the origin site
* title: title of the entry
* summary: a short "first page" summary
* content: the full content of the entry
* date: your date format
* date_iso: date and time of the entry in ISO date format
* date_822 RFC822 date format

If the entry takes place on a date that has no prior entry has
taken place on, the 'new_date' variable is set to that date.
This allows you to break up the page by day.

If the entry is from a different channel to the previous entry,
or is the first entry from this channel on this day
the 'new_channel' variable is set to the same value as the
'channel_url' variable.  This allows you to collate multiple
entries from the same person under the same banner.

Additionally the value of any variable that would be defined
for the channel is available, with 'channel_' prepended to the
name (e.g. 'channel_name' and 'channel_link').

Depending on the feed, there may be a huge variety of other
variables may be available; the best way to find out what you
have is using the 'planet-cache' tool to examine your cache files.

Threading
=========

Updating of feeds can use ``multiprocessing.pool.ThreadPool`` to speed things
up. It can have a significant effect!
See the ``threads`` option in the config file to enable it.

Contributing
------------

My guess is the feature missing from Planet Mars is support
for some templating engine you want.
Just add support for it to ``planet/render.py``,
or put in a ticket and ask me to do it.
It should be really easy to add in support for other rendering
engines than Jinja2 and htmltmpl.

Author
------

Rob Galanakis <rob.galanakis@gmail.com>

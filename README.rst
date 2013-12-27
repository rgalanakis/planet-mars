Planet Mars
-----------

Planet is a flexible feed aggregator.
It downloads news feeds published by web sites and
aggregates their content together into a single combined feed,
latest news first.

This is a fork of the Python planet feed aggregator
originally available at http://www.planetplanet.org/
It is focused on being the simplest Python Planet-based
feed aggregator, much simpler than the original or
more full featured alternatives.

Planet Mars uses Jinja2 for its templating engine,
though htmltmpl (based on Perl's HTML::Template module)
is still supported.
If you want Django or another templating engine,
just put in a ticket,
it should be pretty easy.

Installation
------------

This software is pretty simple and Python 2.6 and
later should work.

To install Planet Mars, you can just use
``pip`` or ``easy_install``.
There are a few dependencies that should be installed
if you don't have them already.
These aren't cutting edge dependencies so even older
versions should be fine.

Compatibility with Python version will depend mostly
on what version of Jinja2 you are going to use.
See Jinja's installation FAQ at
http://jinja.pocoo.org/docs/intro/#prerequisites

Usage
-----

Generally usage is split into two parts:
setup and generation.
Setup is only done when setting up your site,
and generation is done on some schedule.

Setup
&&&&&

1. Copy ``template.ini`` to create your configuration file.
   The ``.ini`` file is heavily commented and should guide
   you through how to customize it.
2. Create your template files for your HTML page or pages.
   The feed templates are provided by Planet,
   you just need to provide your html templates.
3. Create the supporting files your html page links to,
   like images and CSS.
3. Point to your template file(s) from your ``.ini`` file.
4. You're done!

Generation
&&&&&&&&&&

Create some script to call ``python -m planet /path/to/config.ini``
on a schedule.

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

Original Planet Info
--------------------

Planet is a flexible feed aggregator. It downloads news feeds published by
web sites and aggregates their content together into a single combined feed,
latest news first.

It uses Mark Pilgrim's Universal Feed Parser to read from RDF, RSS and Atom
feeds; and Tomas Styblo's templating engine to output static files in any
format you can dream up.

Keywords: feed, blog, aggregator, RSS, RDF, Atom, OPML, Python

Installing Planet
-----------------

You'll need at least Python 2.1 installed on your system, we recommend
Python 2.3 though as there may be bugs with the earlier libraries.

Everything Pythonesque Planet needs should be included in the
distribution.

 i.
    First you'll need to extract the files into a folder somewhere.
    I expect you've already done this, after all, you're reading this
    file.  You can place this wherever you like, ~/planet is a good
    choice, but so's anywhere else you prefer.

 ii.
    Make a copy of the files in the 'examples' subdirectory, and either
    the 'basic' or 'fancy' subdirectory of it and put them wherever
    you like; I like to use the Planet's name (so ~/planet/debian), but
    it's really up to you.

    The 'basic' index.html and associated config.ini are pretty plain
    and boring, if you're after less documentation and more instant
    gratification you may wish to use the 'fancy' ones instead.  You'll
    want the stylesheet and images from the 'output' directory if you
    use it.

 iii.
    Edit the config.ini file in this directory to taste, it's pretty
    well documented so you shouldn't have any problems here.  Pay
    particular attention to the 'output_dir' option, which should be
    readable by your web server and especially the 'template_files'
    option where you'll want to change "examples" to wherever you just
    placed your copies.

 iv.
    Edit the various template (*.tmpl) files to taste, a complete list
    of available variables is at the bottom of this file.

 v.
    Run it: planet.py pathto/config.ini

    You'll want to add this to cron, make sure you run it from the
    right directory.

 vi.
    Tell us about it! We'd love to link to you on planetplanet.org :-)


Template files
--------------

The template files used are given as a space separated list in the
'template_files' option in config.ini.  They are named ending in '.tmpl'
which is removed to form the name of the file placed in the output
directory.

Reading through the example templates is recommended, they're designed to
pretty much drop straight into your site with little modification
anyway.

Inside these template files, <TMPL_VAR xxx> is replaced with the content
of the 'xxx' variable.  The variables available are:

    name	....	} the value of the equivalent options
    link	....	} from the [Planet] section of your
    owner_name .	} Planet's config.ini file
    owner_email	}

    url	....	link with the output filename appended
    generator ..	version of planet being used

    date	....	                         { your date format
    date_iso ...	current date and time in { ISO date format
    date_822 ...	                         { RFC822 date format


There are also two loops, 'Items' and 'Channels'.  All of the lines of
the template and variable substitutions are available for each item or
channel.  Loops are created using <TMPL_LOOP LoopName>...</TMPL_LOOP>
and may be used as many times as you wish.

The 'Channels' loop iterates all of the channels (feeds) defined in the
configuration file, within it the following variables are available:

    name	....	value of the 'name' option in config.ini, or title
    title	....	title retreived from the channel's feed
    tagline ....	description retreived from the channel's feed
    link	....	link for the human-readable content (from the feed)
    url	....	url of the channel's feed itself

    Additionally the value of any other option specified in config.ini
    for the feed, or in the [DEFAULT] section, is available as a
    variable of the same name.

    Depending on the feed, there may be a huge variety of other
    variables may be available; the best way to find out what you
    have is using the 'planet-cache' tool to examine your cache files.

The 'Items' loop iterates all of the blog entries from all of the channels,
you do not place it inside a 'Channels' loop.  Within it, the following
variables are available:

    id	....	unique id for this entry (sometimes just the link)
    link	....	link to a human-readable version at the origin site

    title	....	title of the entry
    summary	....	a short "first page" summary
    content	....	the full content of the entry

    date	....	                              { your date format
    date_iso ...	date and time of the entry in { ISO date format
    date_822 ...                                  { RFC822 date format

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


There are also a couple of other special things you can do in a template.

 -  If you want HTML escaping applied to the value of a variable, use the
    <TMPL_VAR xxx ESCAPE="HTML"> form.

 -  If you want URI escaping applied to the value of a variable, use the
    <TMPL_VAR xxx ESCAPE="URI"> form.

 -  To only include a section of the template if the variable has a
    non-empty value, you can use <TMPL_IF xxx>....</TMPL_IF>.  e.g.

    <TMPL_IF new_date>
    <h1><TMPL_VAR new_date></h1>
    </TMPL_IF>

    You may place a <TMPL_ELSE> within this block to specify an
    alternative, or may use <TMPL_UNLESS xxx>...</TMPL_UNLESS> to
    perform the opposite.

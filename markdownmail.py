#!/usr/bin/python

'''
## What it does now

A command-line tool that takes a Markdown document, templates it as a plaintext email, tags its 
links with Google Analytics parameters and copies its name to the clipboard.

## Doing

* Only tag URLs matching a certain domain

## Todo

* Wrap long text for plaintext emails
* Allow to specify if HTML email wanted (perhaps that should be the default)
* Tag conext with HTML temtplates read from files
'''

import argparse
import sys
import gtk
import re

def cmdline_parse():
	"""Parse the Command-Line arguments and return the options object"""

	# Further documentation at <http://docs.python.org/howto/argparse.html#id1>
	
	parser = argparse.ArgumentParser(
			description = 'Tag and template Markdown text and copy to clipboard.')

	parser.add_argument('--tagdomain', help='domain which should be tagged with Google Analytics, without http://', default='www.bitesizeirishgaelic.com')
	parser.add_argument('filename', help="file in markdown format")
	return parser.parse_args()

def tag_urls(text):
	# Thanks to <http://stackoverflow.com/a/828458/248220>
	traffic_source = "bite_news"
	medium = "email"
	campaign = "newsletter-2000-01-01"
	tags = 'utm_source='+traffic_source+'&utm_medium='+medium+'&utm_campaign='+campaign;
	# urlfinder = re.compile('^(http:\/\/\S+)')
	# urlfinder2 = re.compile('(http:\/\/\S+[^>) \.])')
	urlfinder2 = re.compile('(http:\/\/www.bitesizeirishgaelic.com\S+[^>) \.])')
	# text = urlfinder.sub(r'\1?'+tags, text)
	return urlfinder2.sub(r'\1?'+tags, text)

def template_plain_text(text):
	return "Hi, {!firstname_fix}\n\n"+text

def read_input(filename):
	file = open(filename)
	return file.read()

if __name__ == '__main__':
	cmdline_arguments = cmdline_parse()
	for_output = read_input(cmdline_arguments.filename)
	for_output = template_plain_text(for_output)
	for_output = tag_urls(for_output)

	print for_output
	gtk.Clipboard().set_text(for_output)
	gtk.Clipboard().store()
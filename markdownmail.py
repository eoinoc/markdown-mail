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
	parser.add_argument('--traffic_source', help='traffic source label, such as the name of your email list, for Google Analytics', default='bite_news')
	parser.add_argument('--medium', help='medium of traffic for Google Analytics (default: email)', default='email')
	parser.add_argument('--campaign', help='campaign name for Google Analytics (default: newsletter-2000-01-01)', default='newsletter-2000-01-01')
	parser.add_argument('filename', help="file in markdown format")
	return parser.parse_args()

def tag_urls(text, args):
	# Thanks to <http://stackoverflow.com/a/828458/248220>
	tags = 'utm_source='+args.traffic_source+'&utm_medium='+args.medium+'&utm_campaign='+args.campaign;
	# urlfinder = re.compile('^(http:\/\/\S+)')
	# urlfinder2 = re.compile('(http:\/\/\S+[^>) \.])')
	urlfinder2 = re.compile('(http:\/\/'+args.tagdomain+'\S+[^>) \.])')
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
	for_output = tag_urls(for_output, cmdline_arguments)

	print for_output
	gtk.Clipboard().set_text(for_output)
	gtk.Clipboard().store()
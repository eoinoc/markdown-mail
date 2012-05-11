#!/usr/bin/python

'''
## What it does now

A command-line tool that takes a Markdown document, converts it to HTML (or keeps it as plain text), tags its 
links with Google Analytics parameters and copies its name to the clipboard.

## Doing

* Template content with HTML template files, based on the campaign name
  * Where do we store the template files? Relative to script? Relative to Markdown file? Probably better relative to template file.
  That would mean they're being stored in the same folder/sub-folder for access later on.

  Requirement: subfolder templates/ relative to the Markdown file (by default)

  Question: how to we calculate the path, relative to the provided filename

## Todo

* Wrap long text for plaintext emails
'''

import argparse
import sys
import gtk
import re
import markdown
import os

def cmdline_parse():
	"""Parse the Command-Line arguments and return the options object"""

	# Further documentation at <http://docs.python.org/howto/argparse.html#id1>
	
	parser = argparse.ArgumentParser(description = 'Tag and template Markdown text and copy to clipboard.')
	parser.add_argument('--tagdomain', help='domain which should be tagged with Google Analytics, without http://', default='www.bitesizeirishgaelic.com')
	parser.add_argument('--traffic_source', help='traffic source label, such as the name of your email list, for Google Analytics', default='bite_news')
	parser.add_argument('--medium', help='medium of traffic for Google Analytics (default: email)', default='email')
	parser.add_argument('--campaign', help='campaign name for Google Analytics (default: newsletter-2000-01-01)', default='newsletter-2000-01-01')
	parser.add_argument('--plaintext', help='convert the output for plaintext email (defaults to HTML output)', action='store_true')
	parser.add_argument('filename', help="file in markdown format")
	return parser.parse_args()

def tag_urls(text, args):
	# Thanks to <http://stackoverflow.com/a/828458/248220>
	tags = 'utm_source='+args.traffic_source+'&utm_medium='+args.medium+'&utm_campaign='+args.campaign;
	# urlfinder = re.compile('^(http:\/\/\S+)')
	# urlfinder2 = re.compile('(http:\/\/\S+[^>) \.])')
	urlfinder2 = re.compile('(http:\/\/'+args.tagdomain+'\S+[^">) \.])')
	# text = urlfinder.sub(r'\1?'+tags, text)
	return urlfinder2.sub(r'\1?'+tags, text)

def prepend_greeting(text):
	return "Hi, {!firstname_fix}\n\n"+text

def append_html_header(text, args):
	return read_template(args.filename, 'header')+text

def prepend_html_footer(text, args):
	return text+read_template(args.filename, 'footer')

def to_html(text):
	return markdown.markdown(text)

def read_template(markdown_filename, section):
	markdown_directory = os.path.dirname(os.path.abspath(markdown_filename))
	templates_directory = markdown_directory+'/template'
	template_file = templates_directory+'/'+section+'.html'
	return read_input(template_file)

def read_input(filename):
	file = open(filename)
	return file.read()

if __name__ == '__main__':
	cmdline_arguments = cmdline_parse()
	for_output = read_input(cmdline_arguments.filename)
	for_output = prepend_greeting(for_output)
	if not cmdline_arguments.plaintext:
		for_output = to_html(for_output)
		for_output = append_html_header(for_output, cmdline_arguments)
		for_output = prepend_html_footer(for_output, cmdline_arguments)
	for_output = tag_urls(for_output, cmdline_arguments)

	print for_output
	gtk.Clipboard().set_text(for_output)
	gtk.Clipboard().store()
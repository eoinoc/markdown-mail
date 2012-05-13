#!/usr/bin/python
# coding: utf8

'''
## What it does now

A command-line tool that takes a Markdown document, converts it to HTML (or keeps it as plain text), tags its 
links with Google Analytics parameters and copies its name to the clipboard.

## Doing

* Only tag specified domain

## Todo

* Wrap long text for plaintext emails - change back to the commented-out line which wraps text
'''

import argparse
import sys
import gtk
import re
import markdown
import os
import textwrap

def cmdline_parse():
	"""Parse the Command-Line arguments and return the options object"""

	# Further documentation at <http://docs.python.org/howto/argparse.html#id1>
	
	parser = argparse.ArgumentParser(description = 'Tag and template Markdown text and copy to clipboard.')
	parser.add_argument('--tagdomain', help='domain which should be tagged with Google Analytics, including the protocol such as http://', default='http://www.bitesizeirishgaelic.com')
	parser.add_argument('--traffic_source', help='traffic source label, such as the name of your email list, for Google Analytics (default is directory name that contains your makdown file)')
	parser.add_argument('--medium', help='medium of traffic for Google Analytics (default: email)', default='email')
	parser.add_argument('--plaintext', '-p', help='convert the output for plaintext email (defaults to HTML output)', action='store_true')
	parser.add_argument('filename', help="file in markdown format")
	return parser.parse_args()

def generate_google_analytics_url_params(args):
	traffic_source = extract_traffic_source(args)
	campaign = extract_campaign_name(args.filename)
	return 'utm_source='+traffic_source+'&utm_medium='+args.medium+'&utm_campaign='+campaign;

def tag_urls_with_params(text, domain_to_match, url_params):
	#match_domain = 'http://www.bitesizeirishgaelic.com'
	domain_to_match = re.sub(r'\.', '\.', domain_to_match)

	# Tag URLS like: "[1]: http://www.google.com"
	re_markdown_reference = re.compile(r'(^[ ]{0,3}\[)([^\]]*)(\]: %s\s*[^ ]*)' % domain_to_match, re.MULTILINE)
	text = re.sub(re_markdown_reference, r'\1\2\3?'+url_params, text)

	# Tag URLs like: "<http://www.google.com>"
	re_markdown_inline = re.compile(r'(<%s[^ ]*)(>)' % domain_to_match, re.MULTILINE)
	text = re.sub(re_markdown_inline, r'\1?'+url_params+r'\2', text)

	# Tag URLs like: "[This should be linked.](http://www.google.com)"
	re_markdown_adjacent = re.compile(r'(\[[^\]]+\]\(%s[^\)]*)(\))' % domain_to_match, re.MULTILINE)
	text = re.sub(re_markdown_adjacent, r'\1?'+url_params+r'\2', text)

	return text

def prepend_greeting(text):
	return "Hi, {!firstname_fix}\n\n"+text

def append_html_header(text, args):
	return read_template(args.filename, 'header')+text

def prepend_html_footer(text, args):
	return text+read_template(args.filename, 'footer')

def extract_campaign_name(filename):
	split=os.path.splitext(filename)
	return split[0]

def to_html(text):
	return markdown.markdown(text)

def extract_traffic_source(args):
	traffic_source = ''
	if args.traffic_source:
		traffic_source=args.traffic_source
	else:
		traffic_source=extract_markdown_directory_name(args.filename)
	return traffic_source

def markdown_directory(markdown_filename):
	return os.path.dirname(os.path.abspath(markdown_filename))

def extract_markdown_directory_name(markdown_filename):
	directory = markdown_directory(markdown_filename)
	return os.path.split(directory)[1]

def read_template(markdown_filename, section):
	current_directory = markdown_directory(markdown_filename)
	templates_directory = current_directory+'/template'
	template_file = templates_directory+'/'+section+'.html'
	return read_input(template_file)

def read_input(filename):
	file = open(filename)
	return file.read()

def plaintext_wrap(text):
	'''Wrap a full document of text, not the single paragraph handled by the standard TextWrapper'''
	# # Thanks to <http://code.activestate.com/recipes/358228-extend-textwraptextwrapper-to-handle-multiple-para/>
	# para_edge = re.compile(r"(\n\s*\n)", re.MULTILINE)
	# paragraphs = para_edge.split(text)
	# wrapped_lines = []
	# for paragraph in paragraphs:
	# 	if paragraph.isspace():
	# 		wrapped_lines.append('')
	# 	else:
	# 		for line in textwrap.wrap(paragraph, 79):
	# 		   wrapped_lines.append(line)
	# return '\n'.join(wrapped_lines)

	# Thanks <http://stackoverflow.com/questions/1406493/splitting-a-string-with-no-line-breaks-into-a-list-of-lines-with-a-maximum-colum>
	# return '\n'.join('\n'.join(textwrap.wrap(block, 80)) for block in text.splitlines(True))
	return ''.join(text.splitlines(True))

if __name__ == '__main__':
	cmdline_arguments = cmdline_parse()
	for_output = read_input(cmdline_arguments.filename)
	for_output = prepend_greeting(for_output)
	if cmdline_arguments.plaintext:
		for_output = plaintext_wrap(for_output)
	if not cmdline_arguments.plaintext:
		for_output = to_html(for_output)
		for_output = append_html_header(for_output, cmdline_arguments)
		for_output = prepend_html_footer(for_output, cmdline_arguments)
	domain_to_tag = cmdline_arguments.tagdomain
	google_url_params = generate_google_analytics_url_params(cmdline_arguments)
	for_output = tag_urls_with_params(for_output, domain_to_tag, google_url_params)

	print for_output
	gtk.Clipboard().set_text(for_output)
	gtk.Clipboard().store()

#!/usr/bin/python
# coding: utf8

# Bug: the "campaign" extracts the full path, not just 

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

def tag_marked_url_with_params(html, url_params):
	return re.sub('#tag-google-analtyics', '?'+url_params, html)

def append_html_header(text, args):
	header = read_template(args.filename, 'header')
	url_params = generate_google_analytics_url_params(args)
	header = tag_marked_url_with_params(header, url_params)
	return header+text

def prepend_html_footer(text, args):
	footer = read_template(args.filename, 'footer')
	url_params = generate_google_analytics_url_params(args)
	footer = tag_marked_url_with_params(footer, url_params)
	return text+footer

def extract_campaign_name(filename):
	split=os.path.splitext(os.path.basename(filename))
	return split[0]

def extract_traffic_source(args):
	traffic_source = ''
	if args.traffic_source:
		traffic_source=args.traffic_source
	else:
		traffic_source=extract_markdown_directory_name(args.filename)
	return traffic_source

def to_html(text):
	return markdown.markdown(text)

def markdown_directory(markdown_filename):
	return os.path.dirname(os.path.abspath(markdown_filename))

def extract_markdown_directory_name(markdown_filename):
	directory = markdown_directory(markdown_filename)
	return os.path.split(directory)[1]

def read_template(markdown_filename, section):
	current_directory = markdown_directory(markdown_filename)
	templates_directory = current_directory+'/template'
	template_file = templates_directory+'/'+section+'.html'
	
	output = ''
	if os.path.exists(template_file):
		output = read_input(template_file)
	return output

def read_input(filename):
	file = open(filename)
	return file.read()

def copy_to_clipboard(text):
	gtk.Clipboard().set_text(for_output)
	gtk.Clipboard().store()

if __name__ == '__main__':
	cmdline_arguments = cmdline_parse()
	for_output = read_input(cmdline_arguments.filename)
	domain_to_tag = cmdline_arguments.tagdomain
	google_url_params = generate_google_analytics_url_params(cmdline_arguments)
	for_output = tag_urls_with_params(for_output, domain_to_tag, google_url_params)
	if not cmdline_arguments.plaintext:
		for_output = to_html(for_output)
		for_output = append_html_header(for_output, cmdline_arguments)
		for_output = prepend_html_footer(for_output, cmdline_arguments)
	copy_to_clipboard(for_output)
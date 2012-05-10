#!/usr/bin/python

'''
## What it does now

A command-line tool that takes the name of a Markdown document, and copies
its name to the clipboard.

## What I want it to do

A command-line tool to take a Markdown document and convert it for either
plain-text or HTML email messages.

The result is copied to the clipboard.

Links found in the document are tagged with Google Analytics parameters.
'''

import argparse
import sys
import gtk

def cmdline_parse():
	"""Parse the Command-Line arguments and return the options object"""

	# Further documentation at <http://docs.python.org/howto/argparse.html#id1>
	
	parser = argparse.ArgumentParser(
			description = 'Tag and template Markdown text and copy to clipboard.')
	parser.add_argument("filename", help="file in markdown format")
	return parser.parse_args()

if __name__ == '__main__':
	cmdline_arguments = cmdline_parse()
	gtk.Clipboard().set_text(cmdline_arguments.filename)
	gtk.Clipboard().store()
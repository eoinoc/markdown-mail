# Markdown Mail

For the given Markdown document, tag specified URLs with Google
Analytics parameters and copy to the clipboard.

If the output is to be in HTML (default if -p [plaintext] is 
not specified), then the document is also converted to HTML.

Also for HTML, if the template files
./template/{header,footer}.html are found, the output is also
wrapped with these files.

By default, the basename of the Markdown file is used as the 
campaign name given to Google Analytics.

By default, the name of the folder that contains the Markdown 
file is used as the traffic source value given to Google Analytics.

## Dependencies

* Python's pip package manager. In Debian install it as:

    sudo apt-get install python-pip

* [python-markdown](http://packages.python.org/Markdown/) 
  module. Install it:

    sudo pip install markdown

* Gnome window manager (since my copy-to-clipboard is not 
  platform independent in its current form)

## Usage

python markdownmail.py [campaign-name.markdown]

## License

Copyright (c) 2012 Eoin Ó Conchúir.

Markdown Mail is licensed under The MIT License provided by 
the Open Source Initiative. See the file COPYING for the
license.

## About author

Contact Eoin at <e@eoinoc.net>.

I welcome questions and pullrequests at [this project's
GitHub repo.][1] 

[1]: https://github.com/eoinoc/markdown-mail> 
     "Project on GitHub"

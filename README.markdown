# Markdown Mail

Prepare HTML emails given a Markdown document.

Good if you want to send HTML email.

* Tags specified tags in an email with Google Analytics parameters

* Converts Markdown to HTML (if -p [plaintext] paramter is not
  specified)

* Wraps HTML in specified header and footer template files

* Copies result to clipboard

## Technical details

If the template files `./template/{header,footer}.html` are found, 
then output is also wrapped with these files.

Also see [Premailer](https://github.com/alexdunae/premailer) for
converting normal HTMl/CSS to inline CSS. Run this on your
template files before storing them in the template folder.

By default, the basename of the Markdown file is used as the 
campaign name given to Google Analytics.

By default, the name of the folder that contains the Markdown 
file is used as the traffic source value given to Google Analytics.

## Dependencies

* [python-markdown](http://packages.python.org/Markdown/) 
  module. Install it:

    sudo apt-get install python-pip
    sudo easy_install markdown

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

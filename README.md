# backlinks-ssg

A static site generator for markdown notes that also generates backlinks between files.

![Peek 2021-01-30 09-01](https://user-images.githubusercontent.com/8490222/106352472-55191880-62db-11eb-9213-1ff2ad1c3326.gif)

## Context

I wanted a way of managing backlinks in my markdown notes when I converted them to HTML. I came across someone who wanted to do the exact same thing so I thought I'd take their code as a starting point and re-write it so that it works the way I want.

The code I started from:

- [Build HTML with backlinks via a Makefile](https://web.archive.org/web/20210101134400/https://stackoverflow.com/questions/53798599/how-can-i-build-html-with-a-makefile-with-backlinks)
- [kaihendry/backlinks](https://web.archive.org/web/20210101134414/https://github.com/kaihendry/backlinks)

## Usage

Modify the variables at the top of the Makefile and then once you're
sure that everything is in the right place, just run:
```Bash
make
```
from this git repo and your Markdown files will be turned into a static
site.

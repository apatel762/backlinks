#!/usr/bin/env python

from pandocfilters import toJSONFilter, Link

# Inspired by
# https://web.archive.org/web/20210101195140/https://stackoverflow.com/questions/40993488/convert-markdown-links-to-html-with-pandoc

def change_markdown_links_to_html_links(key, value, format, meta):
  if key == 'Link':
    # links are made up of three parts (https://pandoc.org/lua-filters.html#type-link):
    #   0. attr
    #   1. content
    #   2. target
    # we want the target, and there might be more than one target (somehow)
    # so make sure to select target 0 (the first one) using `[2][0]`
    target = value[2][0]

    # for internal targets, make sure that they now point to HTML files
    # instead of markdown files
    if not target.startswith('http'):
      value[2][0] = target.replace('.md', '.html')

      return Link(value[0], value[1], value[2])

if __name__ == "__main__":
  toJSONFilter(change_markdown_links_to_html_links)
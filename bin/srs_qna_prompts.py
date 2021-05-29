#!/usr/bin/env python

from pandocfilters import toJSONFilter, Para

"""
Convert any 'question' and 'answer' text into text that spans
two lines and will look something like this when viewed in the
HTML:

  Q: What is the answer to this question?
  A: 42

This is so that the Q&A prompts that are scattered throughout
the code become easier to read when converted to HTML (they already
look fine in Markdown)
"""

def reformat_spaced_repetition_text(key, value, format, meta):
  if key == 'Para':
    print('hello world')

if __name__ == "__main__":
  toJSONFilter(reformat_spaced_repetition_text)
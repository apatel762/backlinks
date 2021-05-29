#!/usr/bin/env python

from pandocfilters import Div, Plain, toJSONFilter, attributes

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
    # the spaced repetition text will always start with 'Q:'
    first_word = value[0]['c']
    if first_word == 'Q:':
      # the content of a paragraph is a list of inline elements
      # e.g. links, line breaks, in-line code snippets, text
      started_parsing_answer: bool = False

      para_question = []
      para_answer = []

      for inline in value:
        # there's always a soft line break before the 'A:'
        # once we've seen the soft break, we want to start populating
        # the list containing the inlines that make up the answer
        if inline['t'] == 'SoftBreak':
          started_parsing_answer = True

        if started_parsing_answer:
          para_answer.append(inline)
        else:
          para_question.append(inline)

      # see constructor doc: https://github.com/jgm/pandocfilters/blob/master/pandocfilters.py
      return [
        Div(
          attributes({'class': 'question'}),
          [Plain(para_question)]
        ),
        Div(
          attributes({'class': 'answer'}),
          [Plain(para_answer)]
        )
      ]

if __name__ == "__main__":
  toJSONFilter(reformat_spaced_repetition_text)
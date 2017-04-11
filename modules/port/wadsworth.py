#!/usr/bin/python3
"""
wadsworth.py - Apply Wadsworth's Constant to some text.
https://gist.github.com/1257195
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

def wadsworth(casca, input):
    """.wadsworth - Apply Wadsworth's Constant to some text."""
    text = input.group(2)
    if not text:
        return casca.say(".wadsworth <text> - apply Wadsworth's Constant")

    text = text[text.find(' ', int(round(0.3 * len(text)))) + 1:]
    casca.say(text)
wadsworth.commands = ['wadsworth']

if __name__ == '__main__':
    print(__doc__.strip())

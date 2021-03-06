#!/usr/bin/env python
"""
ping.py - Casca Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://github.com/e7v/casca/
"""

import random

def hello(casca, input): 
    greeting = random.choice(('Hi', 'Hey', 'Hello'))
    punctuation = random.choice(('', '!'))
    casca.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) $nickname[ \t]*$'

def interjection(casca, input): 
    casca.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

if __name__ == '__main__': 
    print(__doc__.strip())

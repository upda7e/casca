# -*- coding: utf8 -*-
'''
imdb.py - casca Movie Information Module
Copyright 2014-2015, Michael Yanovich, yanovich.net
Copyright 2012, Elad Alfassa, <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

This module relies on omdbapi.com

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
'''

from modules import proxy
import json
import re
import urllib2

API_BASE_URL = 'http://www.omdbapi.com/'


def prep_title(txt):
    txt = txt.replace(' ', '+')
    txt = (txt).encode('utf-8')
    txt = urllib2.quote(txt)
    return txt


def movie(casca, input):
    '''.imdb movie/show title -- displays information about a production'''

    if not input.group(2):
        return casca.say('Please enter a movie or TV show title. '
                         'Year is optional.')

    word = input.group(2).rstrip()
    matchObj = re.match(r'([\w\s]*)\s?,\s?(\d{4})', word, re.M | re.I)

    if matchObj:
        title = matchObj.group(1)
        year = matchObj.group(2)
        title = prep_title(title)
        uri = API_BASE_URL + '?t=%s&y=%s&plot=short&r=json' % (title, year)
    else:
        title = word
        title = prep_title(title)
        uri = API_BASE_URL + '?t=%s&plot=short&r=json' % (title)

    try:
        page = proxy.get(uri)
    except:
        return casca.say('[IMDB] Connection to API did not succeed.')

    try:
        data = json.loads(page)
    except:
        return casca.say("[IMDB] Couldn't make sense of information from API")

    message = '[IMDB] '

    if data['Response'] == 'False':
        if 'Error' in data:
            message += data['Error']
        else:
            message += 'Got an error from imdbapi'
    else:
        pre_plot_output = u'Title: {0} | Released: {1} | Rated: {2} '
        pre_plot_output += '| Rating: {3} | Metascore: {4} | Genre: {5} '
        pre_plot_output += '| Runtime: {6} | Plot: '
        genre = data['Genre']
        runtime = data['Runtime']
        pre_plot = pre_plot_output.format(data['Title'], data['Released'],
                                          data['Rated'], data['imdbRating'],
                                          data['Metascore'], genre,
                                          runtime)

        after_plot_output = ' | IMDB Link: http://imdb.com/title/{0}'
        after_plot = after_plot_output.format(data['imdbID'])
        truncation = '[...]'

        ## 510 - (16 + 8 + 63)
        ## max_chars (minus \r\n) - (max_nick_length + max_ident_length
        ##     + max_vhost_lenth_on_freenode)
        max_len_of_plot = 423 - (len(pre_plot) + len(after_plot) + len(truncation))

        new_plot = data['Plot']
        if len(data['Plot']) > max_len_of_plot:
            new_plot = data['Plot'][:max_len_of_plot] + truncation

        message = pre_plot + new_plot + after_plot

    casca.say(message)
movie.commands = ['imdb', 'movie', 'movies', 'show', 'tv', 'television']
movie.example = '.imdb Movie Title, 2015'

if __name__ == '__main__':
    print __doc__.strip()

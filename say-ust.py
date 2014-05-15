#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Ustream 用 ハッシュタグ（メンション）読み上げスクリプト
# 
# Author:   Logi
# URL:      http://logi.hateblo.jp/
# require:  SayKotoeri, Saykana or SayKotoeri2
# OS:       for Mac Only
# Link:     [PythonでTwitterのタイムラインをストリーミングで読み上げさせるfor Mac[tweepy] « haya14busa ](http://haya14busa.com/tweepy-read-aloud-tl/)
# Link:     [twitterをターミナル上で楽しむ(python)](http://www.nari64.com/?p=200)

import tweepy
import logging
import urllib
from subprocess import call
import re
import sys, codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def Setup():
    global mode, name , replace_str
    
    # 0（ハッシュタグ）、1（メンション）
    mode = 0 
    # ハッシュタグもしくはメンションの文字列を指定
    name = 'xxxxx'
    
    replace_str = [
    # 置換する文字列をカンマ区切りで指定
    'Twitter,ツイッター',
    'Ustream,ユーストリーム',
    'Python,パイソン',
    ]
    
    return Setup

def get_oauth():
    CONSUMER_KEY='XXXXXXXXXXXXXXXXXXXX'
    CONSUMER_SECRET='XXXXXXXXXXXXXXXXXXX'
    ACCESS_TOKEN_KEY='XXXXXXXXXXXXXXXXXXX'
    ACCESS_TOKEN_SECRET='XXXXXXXXXXXXXXXXXXX'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth

def str_replace(string):
    string = re.sub('&.+;', ' ', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'URL', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)

    string = re.sub('RT', 'Retweet', string)
    # Ustが追加する文字列を削除
    string = re.sub('\(\#' + name + '[^\)]+\)', '', string)
    # ハッシュタグを削除
    string = re.sub('(?:\#|\uFF03)([a-zA-Z0-9_\u3041-\u3094\u3099-\u309C\u30A1-\u30FA\u3400-\uD7FF\uFF10-\uFF19\uFF20-\uFF3A\uFF41-\uFF5A\uFF66-\uFF9E]+)', '', string)    
    # メンション、リプライを削除
    string = re.sub('@[0-9a-zA-Z_]{1,15}', '', string) 
    
    for buff in replace_str:
        list_value = buff.split(',')
        string = re.sub(list_value[0],list_value[1], string)

    return string

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') :
            try:
                print u'---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                        name = status.author.name,
                        screen = status.author.screen_name,
                        text = status.text,
                        src = status.source,
                        created = status.created_at)
                read_text = str_replace(status.author.name.encode('utf-8')) + 'さん　' + str_replace(status.text.encode('utf-8'))
                call(['SayKotoeri -s "-s 120" "{text}" >/dev/null 2>&1'.format(text=read_text)], shell=True)

            except Exception, e:
                print >> sys.stderr, 'Encountered Exception:', e
                pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def main():
    auth = get_oauth()
    stream = tweepy.Stream(auth, CustomStreamListener())
    Setup()
    if mode : str = '@' + name
    else : str = '#' + name
    stream.filter(track=[str])
    stream.timeout = None

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Ustream 用 ハッシュタグ（メンション）読み上げスクリプト
# 
# Author:   Logi
# URL:      http://logi.hateblo.jp/
# require:  SayKotoeri, Saykana or SayKotoeri2
# OS:       for Mac Only
# Link:     [PythonでTwitterのタイムラインをストリーミングで読み上げさせるfor Mac[tweepy] « haya14busa](http://haya14busa.com/tweepy-read-aloud-tl/)
# Link:     [tweepyでstreamingを使う - 備忘録](http://monowasure78.hatenablog.com/entry/2013/11/26/tweepy%E3%81%A7streaming%E3%82%92%E4%BD%BF%E3%81%86)
# Link:     [tweepyでリアルタイムハッシュタグ検索 — 螺旋階段を一歩ずつ](http://hironow.bitbucket.org/blog/html/2014/01/18/tweepy_hashtag_search.html)

import tweepy
from subprocess import call
import re
import unicodedata
import sys, codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def Setup():
    global mode, name, exception, replace_str
    
    # 0（ハッシュタグ）、1（メンション）
    mode = 0
    # ハッシュタグもしくはメンションの文字列を指定
    name = 'xxxxx'
    # 自分自身のツイートを除外する場合、idを指定
    # （除外しない場合は空白に）
    exception = 'xxxxx'
    
    replace_str = [
    # 置換する文字列をカンマ区切りで指定
    'Twitter,ツイッター',
    'Ustream,ユーストリーム',
    'Ust,ユースト',
    'pixiv,ピクシブ',
    'Pixiv,ピクシブ',
    'Python,パイソン',
    'bot,ボット',
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
    # Ustが追加する文字列を削除
    string = re.sub('\(\s?[#@]' + name + '[^\)]+\)', '', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'URL', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', ' ', string)
    
    string = re.sub('RT', 'Retweet', string)
    # ハッシュタグを削除
    string = re.sub('#[^#\s$]{1,15}', '', string)  
    # メンション、リプライを削除
    string = re.sub('@[0-9a-zA-Z_]{1,15}', '', string)

    # w（ワラ）、8（パチパチ）
    if not (isinstance(string, unicode)):
        string = unicode(string, 'utf-8')
    string= string.replace('\u003d','=')
    string = unicodedata.normalize('NFKC', string)
    match = re.search('([^A-Za-z\s])[wW]', string, re.U)
    if match != None:
        buff = match.group(1)
        string = re.sub('[^A-Za-z\s][wW]', buff + u'ワラ', string)
    string = re.sub('[wW]{2,}', u'ワラワラワラ', string)
    string = re.sub('8{3,}', u'ぱちぱちぱち', string)

    for buff in replace_str:
        list_value = buff.split(',')
        string = string.replace(list_value[0],list_value[1])
    return string

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') or (status.author.screen_name == exception) :
            try:
                print u'---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                        name = status.author.name,
                        screen = status.author.screen_name,
                        text = status.text,
                        src = status.source,
                        created = status.created_at)
                read_text = str_replace(status.author.name.encode('utf-8')) + 'さん　' + str_replace(status.text.encode('utf-8'))
                
                #特殊文字を削除
                read_text = re.sub(ur'[\u2600-\u2687\u2219-\u2761\ue468-\ue5df\uea80-\ueb88\ue63e-\ue6a5\ue6ac-\ue6ae\ue6b1-\ue6ba\ue6ce-\ue757\ue001-\ue05a\ue101-\ue15a\ue201-\ue253\ue301-\ue34d\ue401-\ue44c\ue501-\ue537%s\ue600-\ue619]', '', read_text)
            
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
    Setup()
    if not mode : str = '#' + name
    else : str = '@' + name
    stream = tweepy.Stream(auth, CustomStreamListener(), secure=True)
    stream.filter(languages=['ja'],track=[str])
    stream.timeout = None

if __name__ == "__main__":
    main()
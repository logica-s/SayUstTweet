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
#import unicodedata
import sys, codecs
from tinysegmenter import TinySegmenter

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
    # 読み上げ時に置換する文字列をカンマ区切りで指定
    # パターンには正規表現を使用できます
    #（SayKotoeriに通らない文字は正規表現を使用できません）
    # 正規表現で()の入れ子には非対応
    # 日本語として読ませたい英数字の単語もこちらに記入
    # デフォルトで指定されてるものは削除しないほうが無難です
    u'[Tt]witter,ツイッター',
    u'([Rr]etweet|RT),リツイート',
    u'[Uu]stream,ユーストリーム',
    u'[Uu]st,ユースト',
    u'[Ff]ace[Bb]ook,フェイスブック',
    u'[Pp]ixiv,ピクシブ',
    u'[Yy]ou[Tt]ube,ユーチューブ',
    u'[Ii]nstagram,インスタグラム',
    u'[Aa]ppear,アピアー',
    u'[Aa]ppear.in,アピアー・イン',
    u'[Aa]dobe,アドビ',
    u'[Aa]mazon,あまぞん',
    u'[Mm]acintosh,マッキントッシュ',
    u'[Mm][Aa][Cc],マック',
    u'[Ww]indows,ウィンドーズ',
    u'(LINUX|Linux),リナックス',
    u'[Uu]buntu,ウブントゥ',
    u'[Mm]ac[Bb]ook\s?[Aa]ir,マックブックエアー',
    u'i[Pp]ad,アイパッド',
    u'i[Pp]ad\s?[Aa]ir,アイパッドエアー',
    u'i[Pp]hone,アイフォン',
    u'[Rr]etina,レティーナ',
    u'URL,ユーアールエル',
    u'DVD,ディーブイディー',
    u'SNS,エスエヌス',
    u'OK,オーケー',
    u'TL,ティーエル',
    u'U[Pp],アップ',
    u'[Ww]ord[Pp]ress,ワードプレス',
    u'[Pp]ython,パイソン',
    u'(VOCALOID|Vocaloid),ボーカロイド',
    u'[Bb]ot,ボット',
    u'JR,ジェイアール',
    u'3D,スリーディー',
    u'VS,バーサス',
    u'SF,エスエフ',
    u'SD,エスディー'
    u'SS,エスエス',
    u'PC,ピーシー',
    u'REC,レック',
    u'SCC,エスシーシー',
    u'TOKYO,トーキョー',
    u'V(ita|ITA),ヴィータ',
    u'℃,度',
    u'[RＲ][\-—]18,アールじゅうはち',
    u'(orz|OTL),がっくり',
    u'読み上げ,よみあげ',
    u'(落書き|楽書き|落描き|楽描き|らく書き|らく描き),らくがき',
    u'描い,かい',
    u'描か,かか',
    u'描き,かき',
    u'描け,かけ',
    u'描く,かく',
    u'描こ,かこ',
    u'○,まる',
    u'〇,まる',
    u'●●,まるまる',
    u'静画,せいが',
    u'春色,はるいろ',
    u'夏色,なついろ',
    u'秋色,あきいろ',
    u'冬色,ふゆいろ',
    ]
    
    return Setup

def get_oauth():
    CONSUMER_KEY='XXXXXXXXXXXXXXXXXXXXXXXX'
    CONSUMER_SECRET='XXXXXXXXXXXXXXXXXXXXXXXX'
    ACCESS_TOKEN_KEY='XXXXXXXXXXXXXXXXXXXXXXXX'
    ACCESS_TOKEN_SECRET='XXXXXXXXXXXXXXXXXXXXXXXX'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth

def str_replace(string):

    # Ustが追加する文字列を削除
    string = re.sub('\([#@]' + name + '[^\)]+\)', '', string)
    # remove URL
    string = re.sub('(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', 'URL', string)
    # remove quote
    string = re.sub('"', ' ', string)
    string = re.sub("'", ' ', string)
    string = re.sub('\/', u'／', string)
    
    match = re.compile(r'(^|\s|\d)RT')
    string = match.sub(r'\1Retweet', string)
    # ハッシュタグを削除
    string = re.sub('#[0-9a-zA-Z_]{1,15}(\s|$)', '', string)    
    # メンション、リプライを削除
    string = re.sub('@[0-9a-zA-Z_]{1,15}([^0-9a-zA-Z_])', '', string)

    # Setupでセットした置換。文字によっては正規表現マッチしないので（SayKotoeriに通らない文字）、replaceと処理を分ける
    for buff in replace_str:
        list_value = buff.split(',')
        if (re.match('^[\(\)\[\]\|a-zA-Z\?\*\+\~\$\{\}\\m\\t\\n\\r\\f\\v\\s\\S\\d\\D\\w\\W]+$', list_value[0])) : # 置換指定文字がアルファベットのみ（正規表現含む）
            #日本語内の英語
            match = re.compile('(?:^|[^a-zA-Z\s]|[^a-zA-Z][\s\.,])'+list_value[0]+'(?:[^a-zA-Z\s]|[\s\.,][^a-zA-Z]|$)')
            search = list_value[0].split('|')
            #for m in match.finditer(string) :
            for buff in search :
                search_word = re.sub('[\(\)]', '', buff)
                match = re.compile(u'(^|[^a-zA-Z\s]|[^a-zA-Z][\s\.,])'+search_word+'([^a-zA-Z\s]|[\s\.,][^a-zA-Z]|$)')
                string = match.sub(ur'\1'+list_value[1]+r'\2', string)
        elif (re.search('^[\(\)\[\]\|]$', list_value[0])) : #置換指定文字に日本語が含まれ、かつ正規表現使用
            string = string.replace(list_value[0], list_value[1])
        else : #置換指定文字に正規表現を含まない
            string = re.sub(list_value[0], list_value[1], string)

    # w（ワラ）、8（パチパチ）、TUEEE（つえー）
    if not (isinstance(string, unicode)):
        string = unicode(string, 'utf-8')
    string= string.replace('\u003d','=')
    #string = unicodedata.normalize('NFKC', string)
    match = re.compile(u'([^A-Za-zＡ-Ｚａ-ｚ\s])[wWｗＷ]')
    string = match.sub(u'\1ワラ', string)
    string = re.sub(u'[wWｗＷ]{2,}', u'ワラワラワラ', string)
    match = re.compile(ur'([^A-Za-zＡ-Ｚａ-ｚ\s])[wWｗＷ]')
    string = match.sub(ur'\1ワラ', string)
    string = re.sub('[8８]{3,}', u'ぱちぱちぱち', string)
    string = re.sub('[TＴ][SＳ]?[UＵ][EＥ]{3,}', u'つえーーー', string)
    
    # 日付
    # -- 年月日
    match = re.compile(ur'(?:[1-9][0-9]{3})[\/／\-\.−](?:0[1-9]|[1-9]|1[0-2])[\/／\-\.−](?:0[1-9]|[1-9]|[1-2][0-9]|3[0-1])')
    for m in match.finditer(string) :
        match = re.compile(u'(\D|^)([1-9][0-9]{3})[\/／\-\.−](0[1-9]|[1-9]|1[0-2])[\/／\-\.−](0[1-9]|[1-9]|[1-2][0-9]|3[0-1])(\D|$)')
        string = match.sub(ur'\1\2年\3月\4日\5', string)
    # --月日
    match = re.compile(ur'(?:0[1-9]|[1-9]|1[0-2])[\/／\.−](?:0[1-9]|[1-9]|[1-2][0-9]|3[0-1])')
    for m in match.finditer(string) :
        match = re.compile(u'([^\/／\.−\d]|^)(0[1-9]|[1-9]|1[0-2])[\/／\.−](0[1-9]|[1-9]|[1-2][0-9]|3[0-1])([^\/／\.−\d]|$)')
        string = match.sub(ur'\1\2月\3日\4', string)
    # --数値頭の0を削除
    match = re.compile(u'0(\d)(月|日)')
    string = match.sub(ur'\1\2', string)

    # n分のn
    match = re.compile(ur'(?:[\d]{1,2})[\/／](?:[\d]{1,2})')
    for m in match.finditer(string) :
        match = re.compile(u'([^\/／\d]|^)([\d]{1,2})[\/／]([\d]{1,})(\D|$)')
        string = match.sub(ur'\1\3ぶんの\2\4', string)
    string = re.sub(u'[\/／]', '　', string)

    # バージョン
    match = re.compile(r'[^a-zA-Z][VvＶｖ][eｅ][rｒ][\.．]?([^A-Za-zＡ-Ｚａ-ｚ])')
    string = match.sub(ur'バージョン\1', string)
    
    string = re.sub(u'[\#＃]', u'シャープ', string)
    string = re.sub(u'[$＄]', u'ドル', string)
    string = re.sub(u'[%％]', u'パーセント', string)
    string = string.replace('&amp;', u'アンド')
    string = re.sub(u'&[A-Za-z]{2,6};', ' ', string)
    string = re.sub(u'[&＆]', u'アンド', string)
    string = re.sub(u'[@＠]', u'アット', string)
    
    # SaiKotoeriのエラー対策
    string = string.replace(u'•', u'・')
    string = string.replace('\)', '）')
    string = string.replace('*', u'＊')
    string = re.sub(u'[*⁎⁕]', u'＊', string)
    string = re.sub(u'[⁄⁄\`\´\'｀´\[\]©\|\(\)\{\}\*\․\^]', ' ', string)
    string = re.sub(u'[\_]', u'/', string) # TinySegmenter切り分け対策
    string = string.replace(u'ゐ', u'い')
    string = string.replace(u'ゑ', u'え')
    string = re.sub(u'[づ|ヅ|ﾂﾞ]', u'ず', string)
    match = re.compile(u'(塩|しお)漬け?')
    string = match.sub(ur'\1ずけ', string)
    string = re.sub(u'(浅|あさ)漬け?', u'あさずけ', string)
    match = re.compile(u'気付([いきくけこ])')
    string = match.sub(ur'きず\1', string)
    match = re.compile(u'続([かきくけこ])')
    string = match.sub(ur'つず\1', string)
    string = string.replace(u'卯月', u'うずき')
    string = string.replace(u'文月', u'ふずき')
    string = string.replace(u'葉月', u'はずき')
    string = string.replace(u'神無月', u'かんなずき')
    string = string.replace('三日月', u'みかずき')
    #match = re.compile(u'([\u3400-\u9FFF\uF900-\uFAFF])月([^\u3400-\u9FFF\uF900-\uFAFF])')
    #string = match.sub(ur'\1つき\2', string)
    match = re.compile(u'([\u3400-\u9FFF\uF900-\uFAFF])突き')
    string = match.sub(ur'\1ずき', string)
    string = string.replace('文机', u'ふずくえ')
    match = re.compile(u'([\u3400-\u9FFF\uF900-\uFAFF])机')
    string = match.sub(ur'\1つくえ', string)
    string = match.sub(ur'\1つき\2', string)
    match = re.compile(u'([\u3400-\u9FFF\uF900-\uFAFF])鶴')
    string = match.sub(ur'\1ずる', string)
    match = re.compile(u'([\u3400-\u9FFF\uF900-\uFAFF])妻')
    string = match.sub(ur'\1ずま', string)
    match = re.compile(u'詰め([^てたる]|$)')
    string = match.sub(ur'ずめ\1', string)
    string = string.replace(u'行き詰ま', u'ゆきずま')
    string = string.replace(u'目詰ま', u'目ずま')
    string = re.sub(u'[ぢ|ヂ|痔|ﾁﾞ]', u'じ', string)
    string = re.sub(u'鼻血', u'はなじ', string)
    string = re.sub(u'縮', u'ちじ', string)
    string = string.replace(u'°̥', '')
    match = re.compile(u'(\d+)\-(\d+)')
    string = match.sub(ur'\1−\2', string)
    #string = re.sub('\-', u'−', string)
    string = string.replace('?', u'？')
    
    # 読まれない文字
    string = string.replace(u'髙', u'高')
    string = string.replace(u'♂', u'オス')
    string = string.replace(u'♀', u'メス')
    string = string.replace(u'よめ', u'嫁') # ひらがなの「よ」から「め」への連続はなぜかエラー

    # 読みがアホな文字
    match = re.compile(u'天つ([\u3400-\u9FFF\uF900-\uFAFF])')
    string = match.sub(ur'あまつ\1', string)

    # 拡張数字対策
    string = re.sub(u'[0⓪⓿0︎⃣]', '0', string)
    string = re.sub(u'[1⒈①❶➀➊⓵1︎⃣㊀⑴㈠Ⅰⅰ]', '1', string)
    string = re.sub(u'[2⒉②❷➁➋⓶2︎⃣㊁⑵㈡Ⅱⅱ]', '2', string)
    string = re.sub(u'[3⒊③❸➂➌⓷3︎⃣㊂⑶㈢Ⅲⅲ]', '3', string)
    string = re.sub(u'[4⒋④❹➃➍⓸4︎⃣㊃⑷㈣Ⅳⅳ]', '4', string)
    string = re.sub(u'[5⒌⑤❺➄➎⓹5︎⃣㊄⑸㈤Ⅴⅴ]', '5', string)
    string = re.sub(u'[6⒍⑥❻➅➏⓺6︎⃣㊅⑹㈥Ⅵⅵ]', '6', string)
    string = re.sub(u'[7⒎⑦❼➆➐⓻7︎⃣㊆⑺㈦Ⅶⅶ]', '7', string)
    string = re.sub(u'[8⒏⑧❽➇➑⓼8︎⃣㊇⑻㈧Ⅷⅷ]', '8', string)
    string = re.sub(u'[9⒐⑨❾➈➒⓽9︎⃣㊈㈨Ⅸⅸ]', '9', string)
    string = re.sub(u'[⒑⑩❿➉⓾㊉⑽㈩Ⅹⅹ]', '10', string)
    string = re.sub(u'[⒒⑪⓿⓮⑾Ⅺⅺ]', '11', string)
    string = re.sub(u'[⒓⑫⓬⑿Ⅻⅻ]', '12', string)
    string = re.sub(u'[⒔⑬⓭⒀]', '13', string)
    string = re.sub(u'[⒕⑭⓮⒁]', '14', string)
    string = re.sub(u'[⒖⑮⓯⒂]', '15', string)
    string = re.sub(u'[⒗⑯⓰⒃]', '16', string)
    string = re.sub(u'[⒘⑰⓱⒄]', '17', string)
    string = re.sub(u'[⒙⑱⓲⒅]', '18', string)
    string = re.sub(u'[⒚⑲⓳⒆]', '19', string)
    string = re.sub(u'[⒛⑳⓴⒇]', '20', string)
    string = string.replace('㉑', '21')
    string = string.replace('㉒', '22')
    string = string.replace('㉓', '23')
    string = string.replace('㉔', '24')
    string = string.replace('㉕', '25')
    string = string.replace('㉖', '26')
    string = string.replace('㉗', '27')
    string = string.replace('㉘', '28')
    string = string.replace('㉙', '29')
    string = string.replace('㉚', '30')
    string = string.replace('㉛', '31')
    string = string.replace('㉜', '32')
    string = string.replace('㉝', '33')
    string = string.replace('㉞', '34')
    string = string.replace('㉟', '35')
    string = string.replace('㊱', '36')
    string = string.replace('㊲', '37')
    string = string.replace('㊳', '38')
    string = string.replace('㊴', '39')
    string = string.replace('㊵', '40')
    string = string.replace('㊶', '41')
    string = string.replace('㊷', '42')
    string = string.replace('㊸', '43')
    string = string.replace('㊹', '44')
    string = string.replace('㊺', '45')
    string = string.replace('㊻', '46')
    string = string.replace('㊼', '47')
    string = string.replace('㊽', '48')
    string = string.replace('㊾', '49')
    string = string.replace('㊿', '50')

    string = re.sub(u'[〒〠〶]', u'ゆうびん', string)

    # SayKotoeriでエラーになる文字を削除
    string = re.sub(ur'[^\u0020-\u007E\u0082\u0085\u0091-\u0094\u00A5\u00AB\u00B1\u00BB\u00F7\u2018-\u201F\u203B\u2150-\u218F\u2212-\u2219\u221E\u22EF\u25A0\u25A1\u3001-\u3003\u3005-\u3007\u3012\u3013\u301C\u3020-\u3024\u3033-\u3036\u303B\u303D\u3040-\u30FF\u3400-\u9FFF\uF900-\uFAFF\uFF01-\uFF9F]', u'　', string)

    for buff in replace_str:
        list_value = buff.split(',')
        string = re.sub(list_value[0], list_value[1], string)

    return string

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') or (status.author.screen_name == exception) :
            try:
                print u'\n---{name}/@{screen}---\n   {text}\nvia {src} {created}'.format(
                        name = status.author.name,
                        screen = status.author.screen_name,
                        text = status.text.replace('&amp;','&'),
                        src = status.source,
                        created = status.created_at)
                read_text = str_replace(status.author.name.decode('utf-8')) + 'さん　' + str_replace(status.text.decode('utf-8'))
            
                ts = TinySegmenter()
                result = ts.tokenize(read_text)
                string_jp = ''
                string_en = ''
                for seg in result:
                    seg = re.sub('^\s+', '', seg)
                    if (re.match(u'(?:[^\u0000-\u007F]|[\d+]|^[A-Za-rt-z]{1}$)', seg)) :#日本語が含まれる
                        call(['echo "{text}" | say -v Victoria -r 200 >/dev/null 2>&1'.format(text=string_en)], shell=True)
                        string_en = ''
                        string_jp = string_jp + seg
                    else :
                        call(['SayKotoeri2 -s 110 "{text}" >/dev/null 2>&1'.format(text=string_jp)], shell=True)
                        string_jp = ''
                        string_en = string_en + ' ' + seg

                if(string_jp) :
                    call(['SayKotoeri2 -s 110 "{text}" >/dev/null 2>&1'.format(text=string_jp)], shell=True)
                else :
                    call(['echo "{text}" | say -v Victoria -r 200 >/dev/null 2>&1'.format(text=string_en)], shell=True)

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
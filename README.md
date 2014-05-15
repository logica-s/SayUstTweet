SayUstTweet
===========

Ustream配信時、Twtterのソーシャルストリームを読み上げる（Mac）

1. tweepyをインストール
   $ sudo easy_install tweepy

2. SayKanaをインストール
   こちらから >> http://quickware.a-quest.com/saykana/about.htm

3. Saykotoeriをインストール
   こちらから >> https://sites.google.com/site/nicohemus/home/saykotoeri

4. ハッシュタグorメンション、どちらで動作させるかを指定と、ハッシュタグ（またはメンション＝アカウントid）の文字列を
   コードの該当部分に記入

5. Twitter Developersに登録してCONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRETを
   それぞれ取得してコードの該当位置に記入

6. 任意のフォルダに置いてターミナルから実行
   $ python say-ust.py

enjoy!

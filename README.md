SayUstTweet
===========


[ Ustream配信時、Twtterのソーシャルストリームを読み上げる for Mac ]


※ 要XcodeとCommand Line Tools for Xcodeのインストール、tweepyのインストール


2014/5/22のリリースより、TinySegmenter in Pythonを利用して文章を分割し、日本語OR英語を判別し日本語はSayKotoeri2、英語はsayコマンド（VoiceOver Victoria使用）に渡すようになりました！


1. tweepyをインストール
   $ sudo easy_install tweepy



3. SayKotoeriもしくはSayKotoeri2をインストール


   ( SayKanaをインストール　※ SayKotoeri2を使用する場合は要らない

   こちらから >> http://quickware.a-quest.com/saykana/about.htm )
   
   
   SayKotoeri >> https://sites.google.com/site/nicohemus/home/saykotoeri
   
   SayKotoeri2 >> https://sites.google.com/site/nicohemus/home/saykotoeri2
   
   （デフォルトではSayKotoeri2を使用します。
   
   SayKotoeriを使用する場合はコードの該当部分を書き換えて下さい）


4. TinySegmenter in Python（tinysegmenter.py）をスクリプト本体（say-ust.py）と同じディレクトリに置く
   
   TinySegmenter in Python >> http://lilyx.net/tinysegmenter-in-python/



5. ハッシュタグorメンション、どちらで動作させるかを指定と、ハッシュタグ（またはメンション＝アカウントid）の文字列を
   コードの該当部分に記入


6. Twitter Developersに登録してCONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRETをそれぞれ取得してコードの該当部分に記入


7. 任意のフォルダに置いてターミナルから実行
   $ python say-ust.py


※ PythonのデフォルトエンコーディングをUnicodeに指定しないとエラーが出ます。
   その場合は、お使いのPythonのsite-packagesディレクトリ以下にsitecustomize.pyを作成し、
   
   
   import sys
   
   sys.setdefaultencoding("utf-8")

   encoding = "utf-8"
   
   と記入してください。


enjoy!

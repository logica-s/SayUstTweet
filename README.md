SayUstTweet
===========

[ Ustream配信時、Twtterのソーシャルストリームを読み上げる for Mac ]

1. tweepyをインストール
   $ sudo easy_install tweepy

( 2. SayKanaをインストール ※ SayKotoeri2を使用する場合は要らない

   こちらから >> http://quickware.a-quest.com/saykana/about.htm )

3. SayKotoeriもしくはSayKotoeri2をインストール

   SayKotoeri >> https://sites.google.com/site/nicohemus/home/saykotoeri
   
   SayKotoeri2 >> https://sites.google.com/site/nicohemus/home/saykotoeri2
   
   （デフォルトではSayKotoeri2を使用しますSayKotoeriを使用する場合はコードの該当部分を書き換えて下さい）


4. ハッシュタグorメンション、どちらで動作させるかを指定と、ハッシュタグ（またはメンション＝アカウントid）の文字列を
   コードの該当部分に記入

5. Twitter Developersに登録してCONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRETを
   それぞれ取得してコードの該当位置に記入

6. 任意のフォルダに置いてターミナルから実行
   $ python say-ust.py

※ PythonのデフォルトエンコーディングをUnicodeに指定しないとエラーが出るかもしれません。
   その場合は、お使いのPythonのsite-packagesディレクトリ以下にsitecustomize.pyを作成し、
   
   
   import sys
   sys.setdefaultencoding("utf-8")

   encoding = "utf-8"
   
   と記入してください。



enjoy!

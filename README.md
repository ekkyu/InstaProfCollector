# InstaProfCollector

## Overview
Instagramアカウントのプロフィール情報及びアイコンを抜き出してCSVファイルとimgフォルダに書き出す。

## Description
まず、アカウントIDのリストを用意する。

### user_id.json

usernameを以下のように指定する。

```
[
"ekkkkyu",
"_machico39",
.......................
]
```

次に以下を実行。
```
Python3 instaprofcollector.py
```

## img/

pngファイルのアイコン画像がたまる。

## data.csv

以下のように取得したデータがたまる。

| "key"         | 説明        |
|----------------|---------------|
| "id"         | ユーザID |
| "url"     | アイコンのURL |
| "biography"     | プロフィール文 |
| "country" | 登録した国    |
| "post_num"       | 投稿数    |
| "follow"       | フォロー数    |
| "follower"     | フォロワー数  |
| "hashtag_12post"     | 直近12投稿出現Hashtag  |

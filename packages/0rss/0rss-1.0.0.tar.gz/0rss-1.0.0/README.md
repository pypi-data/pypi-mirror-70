= ハロー・ゼロ =

== 使い方 ==
`pip install 0rss`

Then, simply use the command periodically:

`0rss https://0oo.li/feed/en`

This will save data periodically, to:

`~/.metadrive/data/0rss-0oo.li:default/Post`

== 多源用法 ==

If you want to seprate different sessions and sources, just use name param:

`0rss https://0oo.li/feed/en --name mindey@example.com`

This will save to:
`~/.metadrive/data/0rss-0oo.li:mindey@example.com/Post`

The `--name` value can be arbitray filesystem-compatible filename sub-string, so, you can use it to separate data by accounts, languages, or other features.

**NOTE**: Corresponding auth and session data will be stored in `~/.metadrive/sessions` folder.

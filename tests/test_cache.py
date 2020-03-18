from library import cache
from flask import g


# counter_link = "global:links"
# set_tag = "global:tags"
# set_tag_link = "tag:{}"
# hash_tpl = "links:{}"
def test_save_link(app):
    tags = ['a', 'b']
    title = 'title'
    url = 'url'

    with app.app_context():
        cache.save_link(title, url, tags)
        c = cache.get_cache()
        tag_a_key = cache.set_tag_link.format('a')
        tag_b_key = cache.set_tag_link.format('b')
        hash_key = cache.hash_tpl.format(1)
        assert b'1' == c.get(cache.counter_link)
        assert {b'tag:a', b'tag:b'} == c.smembers(cache.set_tag)
        assert c.sismember(tag_a_key, hash_key)
        assert c.sismember(tag_b_key, hash_key)
        assert {
                   b'id': b'1',
                   b'url': url.encode('utf-8'),
                   b'title': title.encode('utf-8')
               } == c.hgetall(hash_key)

import redis

from flask import current_app, g

counter_link = "global:links"
set_tag = "global:tags"
set_tag_link = "tag:{}"
hash_tpl = "links:{}"


def get_cache():
    if 'cache' not in g:
        g.cache = redis.Redis(
            host=current_app.config['CACHE_HOST'],
            port=current_app.config['CACHE_PORT'],
            db=current_app.config['CACHE_DB']
        )

    return g.cache


def close_cache(e=None):
    if current_app.config['TESTING'] is True:
        g.cache.flushdb()
    cache = g.pop('cache', None)

    if cache is not None:
        cache.close()


def init_app(app):
    app.teardown_appcontext(close_cache)


# INCR global:links
# Loop SADD global:tags tag
# Loop SADD tag:<tag_name> <url_key>
# HMSET <url_key> <url_records>
def save_link(title, url, tags):
    c = get_cache()
    counter = c.get(counter_link)
    if counter is None:
        counter = 0
    counter += 1
    hash_name = hash_tpl.format(counter)
    url_record = {
        "id": counter,
        "title": title,
        "url": url
    }
    p = c.pipeline()
    p.set(counter_link, counter)
    for tag in tags:
        tag_key = set_tag_link.format(tag)
        p.sadd(tag_key, hash_name)
        p.sadd(set_tag, tag_key)
    p.hmset(hash_name, url_record)
    p.execute()

    return url_record

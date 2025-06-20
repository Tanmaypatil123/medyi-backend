import logging
from typing import Dict, Optional, List, Tuple

from django.conf import settings
from redis import Redis
from django_redis import get_redis_connection


def get_cache_key_and_timeout(dict_identifier, **kwargs):
    cache_dict = settings.CACHE_NAMES[dict_identifier]
    cache_key = cache_dict["key"].format(**kwargs)
    if callable(cache_dict["timeout"]):
        cache_timeout = cache_dict["timeout"]()
    else:
        cache_timeout = cache_dict["timeout"]
    return cache_key, cache_timeout


class MyRedisClient:
    def __init__(self):
        self.conn: Redis = get_redis_connection("default")

    def zadd(self, name: str, mapping):
        logging.info(mapping)
        self.conn.zadd(name=name, mapping=mapping)

    def getTopN(self, name: str, top_n: int) -> List[Tuple[str, int]]:
        return self.conn.zrevrange(name=name, start=0, end=top_n, withscores=True)

    def getRank(self, name: str, member: str) -> Tuple[Optional[int], Optional[int]]:
        rank = self.conn.zrevrank(name=name, value=member)
        score = self.conn.zscore(name=name, value=member)
        if rank is not None:
            return int(rank) + 1, score
        else:
            return None, None

    def delete_pattern_matching_keys(self, match):
        list_keys = []
        for key in self.conn.scan_iter(match=match):
            if isinstance(key, bytes):
                key = key.decode("utf-8")
            list_keys.append(key)
        if not list_keys:
            return
        self.conn.delete(*list_keys)

    def get_set_members(self, key: str) -> set:
        return self.conn.smembers(key)

    def add_set_members(self, key: str, members: List, ttl: Optional[int] = None):
        count = 0
        if members:
            count = self.conn.sadd(key, *members)
            if ttl and ttl > 0:
                self.conn.expire(key, ttl)
        return count

    def remove_set_members(self, key: str, members: List):
        if members:
            return self.conn.srem(key, *members)
        return 0

    def remove_zset_member(self, key: str, members: str):
        if members:
            return self.conn.zrem(key, members)
        return 0

    def is_set_members(self, key: str, members: List) -> List[int]:
        if members:
            return self.conn.smismember(key, *members)
        return []

    def set_expire_time(self, name, expire_time):
        # get existing ttl
        self.conn.expireat(name=name, when=expire_time)

    def exists(self, name) -> bool:
        return self.conn.exists(*[name]) > 0

    def ttl(self, key) -> int:
        return self.conn.ttl(key)

    def hgetall(self, key) -> dict:
        return self.conn.hgetall(key)

    def hmset(self, name, mapping: Dict, ttl: Optional[int] = None):
        count = 0
        if mapping:
            count = self.conn.hset(name=name, mapping=mapping)
            if ttl and ttl > 0:
                self.conn.expire(name, ttl)
        return count

    def hsetnx(self, name, key, value):
        return self.conn.hsetnx(name, key, value)

    def hdel(self, name, keys: List):
        return self.conn.hdel(name, *keys)


redis_conn = MyRedisClient()

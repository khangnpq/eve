#coding:utf8
__author__ = 'modm'
import redis
# default values
REDIS_URL = 'redis://localhost:6379'
STATS_KEY = 'scrappy:%(spider)s:%(group)s:stats'
class RedisStatsCollector(object):
    """
        Save stats data in redis for distribute situation.
    """

    def __init__(self, crawler):
        self._dump = crawler.settings.getbool('STATS_DUMP')#default: STATS_DUMP = True
        redis_url = crawler.settings.get('REDIS_URL', REDIS_URL)
        self.stats_key = crawler.settings.get('STATS_KEY', 'scrappy:stats')
        self.server = redis.from_url(redis_url)

    def get_value(self, key, default=None, spider=None):
        if self.server.hexists(self.stats_key,key):
            return int(self.server.hget(self.stats_key,key))
        else:
            return default

    def get_stats(self, spider=None):
        return self.server.hgetall(self.stats_key)

    def set_value(self, key, value, spider=None):
        self.server.hset(self.stats_key,key,value)

    def set_stats(self, stats, spider=None):
        self.server.hmset(self.stats_key,stats)

    def inc_value(self, key, count=1, start=0, spider=None):
        if not self.server.hexists(self.stats_key,key):
            self.set_value(key, start)
        self.server.hincrby(self.stats_key,key,count)

    def max_value(self, key, value, spider=None):
        self.set_value(key, max(self.get_value(key,value),value))

    def min_value(self, key, value, spider=None):
        self.set_value(key, min(self.get_value(key,value),value))

    def clear_stats(self, spider=None):
        self.server.delete(self.stats_key)

    def open_spider(self, spider):
        if hasattr(spider,'tag'):
            self.stats_key = STATS_KEY % {'spider':spider.name,'tag':spider.category or 'default'}
        else:
            self.stats_key = STATS_KEY % {'spider':spider.name,'group':'default'}
        pass
        self.clear_stats(spider=spider)

    def close_spider(self, spider, reason):
        if self._dump:
            spider.logger.info("Dumping Scrapy stats:\n" + str(self.get_stats()))
        self._persist_stats(self.get_stats(), spider)

    def _persist_stats(self, stats, spider):
        pass
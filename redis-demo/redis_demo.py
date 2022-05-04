'''Redis Cache Library'''
# pylint: disable=no-member,import-error,no-name-in-module,broad-except,unused-import
# pylint: disable=invalid-name,too-many-instance-attributes,wrong-import-position
import os
import sys
import ast
import socket
import logging
import redis
import redis_lock
from redis.sentinel import Sentinel

# [redis]
# port = 6379
# search_port = 26379
# master_name = redis-cluster
# life_time = 1800

''' define Python user-defined exceptions'''
class InvalidKey(Exception):
    """Raised when an empty string is used as a key
    to set a key-value pair in the redis server"""

class RedisCache:
    """Class RedisCache"""

    def __init__(self, servers, decode_responses=False, log: logging = logging):
        """
        This method loads the configuration settings
        """
        self.log = log
        self._decode_responses = decode_responses
        self._servers = servers
        self._search_port = 26379
        self._master_name = "redis-cluster"
        self._life_time = 10000
        self._redis_server = self._get_master()
        self._pool = self._get_pool(self._redis_server)

    def _get_master(self):
        """Finds the Master Node and PORT for the redis"""
        master = None
        for server in self._servers:
            self.log.info(f"trying server ({server})")
            sentinel_conf = [(server, self._search_port)]
            try:
                sentinel = Sentinel(sentinel_conf, socket_timeout=5)
                master = sentinel.discover_master(self._master_name)
                break
            except Exception as e:
                self.log.critical(f'Redis server {server} down ' + str(e))
        if not master:
            self.log.critical('Unable to connect to any redis server to get master')
            raise ConnectionError('Unable to connect to any redis server to get master')

        self.log.info("redis master server:" + str(master[0]))
        return master

    def _get_pool(self, master):
        """Gets a connection pool to the redis master"""
        redis_host = master[0]
        redis_port = master[1]
        try:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port,
                                        db=0, decode_responses=self._decode_responses)
            return redis.Redis(connection_pool=pool)
            # return redis.StrictRedis(host=redis_host, port=redis_port,
            #                          db=0, decode_responses=True)
        except Exception as e:
            self.log.critical('connection to redis failed[%s]' % e)
            raise ConnectionError(str(e))

    def ping(self):
        """
        Checks the connectivity to the Redis Master
        :return:
        """
        self.log.info('Pinging redis to checking connectivity')
        return self._pool.ping()

    def set_key(self, key, value, life_time=None):
        """
        This method sets a key in the redis server to a value with a default 30 min lifetime

        Args:
            redis_server:
            key:
            value:
            life_time:

        Returns:

        """
        if not life_time:
            life_time = self._life_time
        if not key:
            raise InvalidKey("Invalid key used. Key must be non empty.")
        status = self._pool.set(key, value, ex=life_time)
        return status

    def get_key(self, key):
        """
        This method get the value of a key from the redis server

        Args:
            redis_server:
            key:

        Returns:

        """
        return self._pool.get(key)

    def delete_key(self, cache_key):
        """
        This method deletes the given key from the redis server
        :param: key:
        :return:
        """
        value_type = str(self._pool.type(cache_key))
        if value_type == 'list':
            value = self.rpop(cache_key)
        else:
            value = self.get_key(cache_key)
        if value:
            self._pool.delete(cache_key)
            return value
        return False

    def append_key(self, cache_key, value):
        '''
        This method concatenates the string value with the value already present
        corresponding to the key, if key is present else creates a new key-value pair
        :param cache_key:
        :param value:
        :return:
        '''
        value = self._pool.append(cache_key, value)
        return value

    def rpush(self, cache_key, *value):
        '''
        This method appends the value arguments to the list corresponding to
        the given key in the redis server
        :param cache_key:
        :param value:
        :return:
        '''
        return self._pool.rpush(cache_key, *value)

    def rpop(self, cache_key):
        '''
        This method pops the last element of the list corresponding to the
        given key in the redis server
        :param cache_key:
        :return:
        '''
        value = self._pool.rpop(cache_key)
        return value

    def lrange(self, cache_key, start=0, stop=100):
        '''
        This method returns a list of values within given index range
        corresponding to the given key in the redis server
        :param cache_key:
        :param start:
        :param stop:
        :return:
        '''
        value = self._pool.lrange(cache_key, start, stop)
        return value

    def lrem(self, cache_key, count, value):
        '''
        This method removes count no of elements matching the value
        from the list corresponding to the given key in the redis server
        :param cache_key:
        :param count:
        :param value:
        :return:
        '''
        return self._pool.lrem(cache_key, count, value)

    def get_all_keys(self, pattern: str = '*'):
        '''
        This methods returns all the keys present in the redis server which
        matches the given pattern
        :param pattern:
        :return:
        '''
        return self._pool.keys(pattern=pattern)

    def expire(self, key, time):
        '''
        This methods sets the remaining lifetime of the given key
         after which the key ceases to exist in the redis server
        :param key:
        :param time:
        :return:
        '''
        return self._pool.expire(key, time)

    def time_to_live(self, key):
        """
        This methods returns the remaining lifetime of a key in the
        redis server.
        :param key:
        :return:
        """
        return self._pool.ttl(key)

    def lock(self, lock_name: str, lock_timeout: int = 1): # pragma: no cover
        """
        This method get a lock lock_name and holds it for lock_timeout seconds or until it's unlocked
        Args:
            lock_name:
            lock_timeout: in seconds
        Returns:
        """
        lock = redis_lock.Lock(self._pool, lock_name, id="1", expire=lock_timeout)
        if lock.acquire(blocking=False):
            self.log.info(f"Got the lock {lock_name}")
        else:
            msg = f'The resource is already acquired: {lock_name}'
            self.log.critical(msg)
            raise Exception(msg)

    def unlock(self, lock_name: str): # pragma: no cover
        """
        This method releases the lock lock_name
        Returns:
        """
        try:
            lock = redis_lock.Lock(self._pool, lock_name, id="1")
            lock.release()
            self.log.info("lock released: " + lock_name)
        except Exception as e:
            self.log.info("not locked: " + lock_name)

if __name__ == '__main__':

    # redisf = RedisCache()
    # redis_server = redisf.get_server()
    # status = redisf.get_key('testme')
    # print("status:" + str(status))
    # status = redisf.set_key('testme1', 'value1', 100)
    # print("status:" + str(status))
    # status = redisf.get_key('testme1')
    # keys = redisf.get_all_keys(pattern='is-os-obsolete*')
    # for key in keys:
    #     print(key)
    #     # redisf.delete_key(cache_key=key)
    # print("status:" + status)

    redisf = RedisCache(servers=["ITSUSRALSP06927", "ITSUSRALSP07062"])
    print(redisf.ping())

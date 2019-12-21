import logging

from kvs.util import Singleton


logger = logging.getLogger(__name__)

class KeyValueStore(metaclass=Singleton):

    def __init__(self):
        self.dictionary = {}

    def set(self, key, value):
        """Sets a key to a particular value"""
        self.dictionary[key] = value
        logger.info(f'SET {key}: {value}')
        return True

    def get(self, key):
        """Fetch the data stored at the given key"""
        if key in self.dictionary:
            logger.info(f'GET {key}: success')
            return self.dictionary[key]
        else:
            logger.info(f'GET {key}: does not exist')
            return None

    def delete(self, key):
        """Delete the value stored at the given key"""
        if key in self.dictionary:
            del self.dictionary[key]
            logger.info(f'DELETE {key}: success')
            return True
        else:
            logger.info(f'DELETE {key}: does not exist')
            return False
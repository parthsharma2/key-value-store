import logging

from kvs.util import Singleton


logger = logging.getLogger(__name__)

class KeyValueStore(metaclass=Singleton):

    def __init__(self):
        """Key Value Store capable of getting/setting/deleting key-value pairs."""
        self.dictionary = {}

    def set(self, key, value):
        """Set a key to a particular value.

        :param key: The key to set the value to.
        :param value: The value to assign to the key.
        :return: True if success, False if failure
        :rtype: bool
        """
        try:
            self.dictionary[key] = value
            logger.info(f'SET {key}: {value}')
            return True
        except Exception as e:
            logger.info(f'SET {key}: {value} failed')
            logger.exception(e)
            return False

    def get(self, key):
        """Fetch the data stored at the given key.

        :param key: The key to fetch the value of.
        :return: Value of the key, if it exists, else None
        """
        if key in self.dictionary:
            logger.info(f'GET {key}: success')
            return self.dictionary[key]
        else:
            logger.info(f'GET {key}: does not exist')
            return None

    def delete(self, key):
        """Delete the value stored at the given key.

        :param key: The key to delete.
        :return: True if key exists and deleted else False
        :rtype: bool
        """
        if key in self.dictionary:
            del self.dictionary[key]
            logger.info(f'DELETE {key}: success')
            return True
        else:
            logger.info(f'DELETE {key}: does not exist')
            return False

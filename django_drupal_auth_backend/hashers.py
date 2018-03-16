import hashlib
import sys

from collections import OrderedDict

from django.contrib.auth.hashers import BasePasswordHasher
from django.contrib.auth.hashers import mask_hash
from django.utils.translation import gettext_noop as _


if sys.version_info[0] < 3:
    # python 2
    raise NotImplementedError('this package does not work with python2')


ITOA64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
DEFAULT_ITERATION_CODE = 'C'
SALT_LENGTH = 8


class DrupalPasswordHasher(BasePasswordHasher):

    algorithm = 'drupal_sha512'

    def verify(self, password, encoded):
        hash = encoded.split("$")[1]
        iter_code = hash[0]
        salt = hash[1:1 + SALT_LENGTH]
        return encoded == self.encode(password, salt, iter_code)

    def safe_summary(self, encoded):
        algorithm, remainder = encoded.split('$')
        iterations = self.get_iteration_count(remainder[0])
        salt = remainder[1:9]
        hash = remainder[9:]
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('iterations'), iterations),
            (_('salt'), mask_hash(salt)),
            (_('hash'), mask_hash(hash)),
        ])

    def get_iteration_count(self, code):
        return 2 ** ITOA64.index(code)

    def encode(self, password, salt, iter_code=None):
        # converted to Python3 from Drupal's _password_crypt()
        if iter_code is None:
            iter_code = DEFAULT_ITERATION_CODE
        iterations = self.get_iteration_count(iter_code)
        password = password.encode('utf-8')
        hash = hashlib.sha512(salt.encode('utf-8') + password).digest()
        for i in range(iterations):
            hash = hashlib.sha512(hash + password).digest()
        hash = self.base_64_encode(hash)
        encoded = '{0}${1}{2}{3}'.format(self.algorithm, iter_code, salt, hash)
        return encoded[:66]

    def base_64_encode(self, input):
        # converted to Python3 from Drupal's _password_base64_encode()
        count = len(input)
        output = ''
        i = 0
        while i < count:
            value = input[i]
            i = i + 1
            output += ITOA64[value & 0x3f]
            if i < count:
                value |= input[i] << 8
            output += ITOA64[(value >> 6) & 0x3f]
            if i >= count:
                break
            i += 1
            if i < count:
                value |= input[i] << 16
            output += ITOA64[(value >> 12) & 0x3f]
            if i >= count:
                break
            i += 1
            output += ITOA64[(value >> 18) & 0x3f]
        return output

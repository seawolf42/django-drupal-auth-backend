import sys
import unittest

from django_drupal_auth_backend import hashers

if sys.version_info[0] < 3:
    # python 2
    raise NotImplementedError('this package does not work with python2')

from unittest import mock  # noqa F402


test_base_64_encodes = (
    (
        b'\x7f-\xfeG\x0ba\x01b\x92\x95\xbc\xddV\xd9\xe3\x93\xf3Ya[\xe3\xf7\xf3\xa5\xea\xe6{\x85(\x8a\x83B\xd2\xd8x\xd1!\x91~\xf6DO<\x8fk\xcb\x18Fk\t>a^\x95\xcb\xfal?*\x82l\xb4.\x90',  # noqa
        'zpWz5hEM/6aYJmPrKZxsHCTKVhpsrDTdePyS3WWW18YoMXLoV2dTqHoHwwsO9XVFfZUDVtJZ9fDPzcWUgFf9E0',
    ),
    (
        b'\x0e\x94\xc82\\\xda\xec\xba\xec\x01\xb1\x96\x8b\xaeLa\x83KRFn\x83#\xda\xd6\xa3\xb3s\x90\xa5\xd9]d\'\x89\xe0k\xd3oo\xbbg\x06\x19\x83\xed=R\xf7\x12\xba\xd5\xb7\x99\xe5\x14n\x91i?]\x93\x0e\xbd',  # noqa
        'CE7mmkZqgf9v/2fZ9u8HVBsGGNYP1CWqKDugn/NdNr3NbY6sfBxPjhvN4YlUhrXIr9ViJTPaZHVPFaqDRBd1x0',
    ),
    (
        b'\\\xe3\xd0\r\x8aH\xcd\x96\xdbv\xb6\x90\x11W1X\x98\x88-\xbf\xab\xc4\xf2\xa3\x86\x05\x18\xf8\xf5.\xe6\x1cu&\xec\xcf\xfd\xbd\x06P\xe6\xfe\xa7\xe7\xdec;\xec\x81z\x1b\xd2\xc9\x82\x89\xd9\x93R;z\xd7\xfa\xc6\xe1',  # noqa
        'QBCoBc6GBPtqqN9YFQJAMV7Whwve29zc4K.4sLj9anFRakynxrf/ENizbSirXh1v/er4GbgU7axYGhXSLfjlV1',
    ),
    (
        b'f\xb2\x80|$\x0b\xe3\xf0\xd6=\xe8\x0b\xfa\x19\x16\xce\xb8\x06tx\xf3W\xb5_\x0cL\x13\xbaw\xd7\xdf:,O(\xd0\x9dK\xff\xd1\x1c\x98\xb0Vtw*\x9b\x04<\xf1%\x18\xd4\x19\xe9\xab\xe0\x8c5\x08\xbf\xa9\xc8',  # noqa
        'a79UwFm0X1jpxUy0ubV3CXf/oVrwLJvLAko2uSrpTf19DV0oRiozFn/akO3Rrdma2kHwZU/pNYyeUnMB6wPe61',
    ),
)


class DrupalPasswordHasherTest(unittest.TestCase):

    def setUp(self):
        self.hasher = hashers.DrupalPasswordHasher()

    def test_hash_calls_get_iteration_count(self):
        self.hasher.get_iteration_count = mock.MagicMock()
        self.hasher.encode('password', 'SALT', 'D')
        self.hasher.get_iteration_count.assert_called_once_with('D')

    def test_hash_calls_get_iteration_count_default(self):
        self.hasher.get_iteration_count = mock.MagicMock()
        self.hasher.encode('password', 'SALT')
        self.hasher.get_iteration_count.assert_called_once_with('C')

    @mock.patch('hashlib.sha512')
    def test_encode(self, mock_sha512):
        self.hasher.get_iteration_count = mock.MagicMock(return_value=0)
        self.hasher.base_64_encode = mock.MagicMock(return_value='HASH')
        sha512_return_value = mock.MagicMock()
        sha512_return_value.digest = mock.MagicMock(return_value='SHA512DIGEST')
        mock_sha512.return_value = sha512_return_value
        self.assertEqual(self.hasher.encode('password', 'SALT', 'ITERATIONS'), 'drupal_sha512$ITERATIONSSALTHASH')
        self.hasher.get_iteration_count.assert_called_once_with('ITERATIONS')
        self.hasher.base_64_encode.assert_called_once_with('SHA512DIGEST')

    @mock.patch('django_drupal_auth_backend.hashers.mask_hash')
    @mock.patch('django_drupal_auth_backend.hashers._')
    def test_safe_summary_a(self, mock_gettext, mock_mask_hash):
        def return_same(value):
            return value
        mock_mask_hash.side_effect = return_same
        mock_gettext.side_effect = return_same
        summary = self.hasher.safe_summary('drupal_sha512$CSSAALLTTHASH')
        self.assertEqual(summary['algorithm'], 'drupal_sha512')
        self.assertEqual(summary['iterations'], 16384)
        self.assertEqual(summary['salt'], 'SSAALLTT')
        self.assertEqual(summary['hash'], 'HASH')

    def test_iteration_count_dot(self):
        self.assertEqual(self.hasher.get_iteration_count('.'), 1)

    def test_iteration_count_slash(self):
        self.assertEqual(self.hasher.get_iteration_count('/'), 2)

    def test_iteration_count_zero(self):
        self.assertEqual(self.hasher.get_iteration_count('0'), 4)

    def test_iteration_count_cap_a(self):
        self.assertEqual(self.hasher.get_iteration_count('A'), 4096)

    def test_iteration_count_cap_l(self):
        self.assertEqual(self.hasher.get_iteration_count('L'), 8388608)

    def test_iteration_count_small_a(self):
        self.assertEqual(self.hasher.get_iteration_count('a'), 274877906944)

    def test_iteration_count_small_z(self):
        self.assertEqual(self.hasher.get_iteration_count('z'), 9223372036854775808)

    def test_convert_inputs_to_base64(self):
        for binary, base64 in test_base_64_encodes:
            self.assertEqual(self.hasher.base_64_encode(binary), base64)

    def test_full_encodings(self):
        self.assertEqual(
            self.hasher.encode('password', 'saltsalt', 'C'),
            'drupal_sha512$CsaltsaltA112iY375iFdNhp.gYEWxwlWtXdhjl.8hY7BufRTJ1u',
        )
        self.assertEqual(
            self.hasher.encode('mypassword', 'YEWxwlWt', 'F'),
            'drupal_sha512$FYEWxwlWtUUj8uB5QN2K0X9lNrnRl/hLpN3Qp8GK7v8emyc9eRsf',
        )

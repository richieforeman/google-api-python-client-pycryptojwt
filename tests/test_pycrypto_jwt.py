#!/usr/bin/python2.4

"""Oauth2client tests

Unit tests for oauth2client.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'
__author__ = 'richie.foreman@gmail.com'


import os
import sys
import tempfile
import time
import unittest

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from apiclient.http import HttpMockSequence
from oauth2client.anyjson import simplejson
from oauth2client.client import Credentials

from oauth2client.client import _urlsafe_b64decode
from PyCryptoSignedJWT import PyCryptoSignedJwtAssertionCredentials
from PyCryptoSignedJWT import PyCryptoSigner
from PyCryptoSignedJWT import PyCryptoVerifier
from PyCryptoSignedJWT import verify_signed_jwt_with_certs
from PyCryptoSignedJWT import _urlsafe_b64decode, _urlsafe_b64encode
from PyCryptoSignedJWT import verify_id_token

from oauth2client.file import Storage


from oauth2client.client import make_signed_jwt


def datafile(filename):
    f = open(os.path.join(os.path.dirname(__file__), 'data', filename), 'r')
    data = f.read()
    f.close()
    return data


class CryptTests(unittest.TestCase):

    def test_sign_and_verify(self):
        private_key = datafile('privatekey.pem')
        public_key = datafile('privatekey.pem')

        signer = PyCryptoSigner.from_string(private_key)
        signature = signer.sign('foo')
        self.assertIsNot(False, signature)
        print signature

        #verifier = crypt.Verifier.from_string(public_key, True)

        #self.assertTrue(verifier.verify('foo', signature))

        #self.assertFalse(verifier.verify('bar', signature))
        #self.assertFalse(verifier.verify('foo', 'bad signagure'))

    def _check_jwt_failure(self, jwt, expected_error):
        try:
            public_key = datafile('publickey_der')
            certs = {'foo': public_key}
            audience = 'https://www.googleapis.com/auth/id?client_id=' +\
                       'external_public_key@testing.gserviceaccount.com'
            contents = verify_signed_jwt_with_certs(jwt, certs, audience)
            self.fail('Should have thrown for %s' % jwt)
        except:
            e = sys.exc_info()[1]
            msg = e.args[0]
            print e
            self.assertTrue((expected_error in msg))

    def _create_signed_jwt(self):
        private_key = datafile('privatekey.pem')


        signer = PyCryptoSigner.from_string(private_key)
        audience = 'some_audience_address@testing.gserviceaccount.com'
        now = long(time.time())

        return make_signed_jwt(
            signer,
                {
                'aud': audience,
                'iat': now,
                'exp': now + 300,
                'user': 'billy bob',
                'metadata': {'meta': 'data'},
                })

    def test_verify_id_token(self):
        jwt = self._create_signed_jwt()
        public_key = datafile('publickey_der')
        certs = {'foo': public_key }
        audience = 'some_audience_address@testing.gserviceaccount.com'
        contents = verify_signed_jwt_with_certs(jwt, certs, audience)
        self.assertEqual('billy bob', contents['user'])
        self.assertEqual('data', contents['metadata']['meta'])

    def test_verify_id_token_with_certs_uri(self):
        # This is really only used for AppIdentity-type calls
        pass

    def test_verify_id_token_with_certs_uri_fails(self):
        # This is really only used for AppIdentity-type calls
        pass

    def test_verify_id_token_bad_tokens(self):
        private_key = datafile('privatekey.pem')

        # Wrong number of segments
        self._check_jwt_failure('foo', 'Wrong number of segments in token: foo')

        # Not json
        self._check_jwt_failure('foo.bar.baz','Can\'t parse token')

        # Bad signature
        jwt = 'foo.%s.baz' % _urlsafe_b64encode('{"a":"b"}')
        self._check_jwt_failure(jwt, 'No iat field in token')

        # No expiration
        signer = PyCryptoSigner.from_string(private_key)
        audience = 'https:#www.googleapis.com/auth/id?client_id=' +\
                   'external_public_key@testing.gserviceaccount.com'
        jwt = make_signed_jwt(signer, {
            'aud': 'audience',
            'iat': time.time(),
            }
        )
        self._check_jwt_failure(jwt, 'No exp field in token')

        # No issued at
        jwt = make_signed_jwt(signer, {
            'aud': 'audience',
            'exp': time.time() + 400,
            }
        )
        self._check_jwt_failure(jwt, 'No iat field in token')

        # Too early
        jwt = make_signed_jwt(signer, {
            'aud': 'audience',
            'iat': time.time() + 301,
            'exp': time.time() + 400,
            })
        self._check_jwt_failure(jwt, 'Token used too early')

        # Too late
        jwt = make_signed_jwt(signer, {
            'aud': 'audience',
            'iat': time.time() - 500,
            'exp': time.time() - 301,
            })
        self._check_jwt_failure(jwt, 'Token used too late')

        # Wrong target
        jwt = make_signed_jwt(signer, {
            'aud': 'somebody else',
            'iat': time.time(),
            'exp': time.time() + 300,
            })
        self._check_jwt_failure(jwt, 'Wrong recipient')


class SignedJwtAssertionCredentialsTests(unittest.TestCase):

    def test_credentials_good(self):
        private_key = datafile('privatekey.pem')
        credentials = PyCryptoSignedJwtAssertionCredentials(
            'some_account@example.com',
            private_key,
            scope='read+write',
            prn='joe@example.org')
        http = HttpMockSequence([
            ({'status': '200'}, '{"access_token":"1/3w","expires_in":3600}'),
            ({'status': '200'}, 'echo_request_headers'),
        ])
        http = credentials.authorize(http)
        resp, content = http.request('http://example.org')
        self.assertEqual('Bearer 1/3w', content['Authorization'])

    def test_credentials_to_from_json(self):
        private_key = datafile('privatekey.pem')
        credentials = PyCryptoSignedJwtAssertionCredentials(
            'some_account@example.com',
            private_key,
            scope='read+write',
            prn='joe@example.org')
        json = credentials.to_json()
        print json
        restored = Credentials.new_from_json(json)
        print restored.to_json()
        self.assertEqual(credentials.private_key, restored.private_key)
        self.assertEqual(credentials.private_key_password,
                         restored.private_key_password)
        self.assertEqual(credentials.kwargs, restored.kwargs)

    def _credentials_refresh(self, credentials):
        http = HttpMockSequence([
            ({'status': '200'}, '{"access_token":"1/3w","expires_in":3600}'),
            ({'status': '401'}, ''),
            ({'status': '200'}, '{"access_token":"3/3w","expires_in":3600}'),
            ({'status': '200'}, 'echo_request_headers'),
        ])
        http = credentials.authorize(http)
        resp, content = http.request('http://example.org')
        return content

    def test_credentials_refresh_without_storage(self):
        private_key = datafile('privatekey.pem')
        credentials = PyCryptoSignedJwtAssertionCredentials(
            'some_account@example.com',
            private_key,
            scope='read+write',
            prn='joe@example.org')

        content = self._credentials_refresh(credentials)

        self.assertEqual('Bearer 3/3w', content["Authorization"])

    def test_credentials_refresh_with_storage(self):
        private_key = datafile('privatekey.pem')
        credentials = PyCryptoSignedJwtAssertionCredentials(
            'some_account@example.com',
            private_key,
            scope='read+write',
            prn='joe@example.org')

        (filehandle, filename) = tempfile.mkstemp()
        os.close(filehandle)
        store = Storage(filename)
        store.put(credentials)
        credentials.set_store(store)
        content = self._credentials_refresh(credentials)

        self.assertEqual('Bearer 3/3w', content['Authorization'])
        os.unlink(filename)


if __name__ == '__main__':
    unittest.main()
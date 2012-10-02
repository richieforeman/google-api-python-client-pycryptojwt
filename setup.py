#!/usr/bin/env python

from distutils.core import setup

import os
def read(fname):
     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='PyCryptoSignedJWT',
     version='0.1',
     description='Utility to allow signing JWT assertion credentials using PyCrypto.',
     long_descriotion=read('README.md'),
     author='Chris Targett',
     author_email='chris@xlevus.net',
     url='http://github.com/xlevus/google-api-python-client-pycryptojwt',
     py_modules = ['PyCryptoSignedJWT'],
     install_requires = ['PyCrypto>=2.6'],
     classifiers=[
     ],
     keywords='appengine pycrypto google-api',
     license='',
)

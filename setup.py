#! /usr/bin/env python
import os
from setuptools import setup

import admin_sso
setup(
    name='django-admin-sso',
    version=admin_sso.__version__,
    description='django sso solution',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Marc Egli',
    author_email='egli@allink.ch',
    url='http://github.com/frog32/django-admin-sso/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'admin_sso',
        'admin_sso.openid',
    ],
    # package_data={'admin_sso':'templates/*.html'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=(
        'Django>=1.4',
        'oauth2client>=1.2',
    ),
    include_package_data=True,
)

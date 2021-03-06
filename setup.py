# -*- coding: utf-8 -*-
"""Installer for the video.converter package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='video.converter',
    version='1.0a1',
    description="This package provides Video Dexterity Content Type for conversions when upload and players/views.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='alberto.duran',
    author_email='alberto.duran@ithinkupc.com',
    url='https://pypi.python.org/pypi/video.converter',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['video'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.transformchain',
        'plone.app.dexterity',
        'plone.autoform',
        'plone.app.textfield',
        'plone.app.blob',
        'plone.rfc822',
        'plone.supermodel',
        'five.globalrequest',
        'plone.api',
        'Products.GenericSetup>=1.8.2',
        'z3c.jbot',
        'requests'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = video.converter.locales.update:update_locale
    """,
)

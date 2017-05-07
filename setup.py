import os
import codecs
from setuptools import setup, find_packages

parent_dir = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(parent_dir, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='cachspeak',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='Cachet to TeamSpeak integration bot',
    long_description=long_description,

    author='Enrico Ghidoni',
    author_email='enricoghdn@gmail.com',

    license='BSD 3-Clause License',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: System Administrators',

        'Topic :: Communications :: Chat',
        'Topic :: Utilities',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='cachet teamspeak bot',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'ts3==1.0.5',
        'python-cachetclient==0.2.3'
    ],

    extras_requires={
        'test': [
            'coverage>=4.3,<5',
            'pytest>=3,<4',
            'pytest-cov>=2.4,<3',
            'pytest-mock>=1.6,<2'
        ]
    },

    entry_points={
        'console_scripts':[
            'cachspeak=cachspeak:cli_entry_point',
        ],
    },
)
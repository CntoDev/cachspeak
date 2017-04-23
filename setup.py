import os
import codecs
from setuptools import setup, find_packages

parent_dir = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(parent_dir, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='cachspeak',

    version='1.0.0dev0',

    description='Cachet to TeamSpeak integration bot',
    long_description=long_description,

    # TODO: once repository is up uncomment
    # url='https://github.com/enricoghdn/cachspeak',

    author='Enrico Ghidoni',
    author_email='enricoghdn@gmail.com',

    license='BSD 3-Clause License',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

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

    entry_points={
        'console_scripts':[
            'cachspeak=cachspeak:cli_entry_point',
        ],
    },
)
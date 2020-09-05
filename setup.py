# -*- coding: utf-8 -*-
"""
Lucas Ou 2014 -- http://lucasou.com

Setup guide: http://guide.python-distribute.org/creation.html
python setup.py sdist bdist_wininst upload
"""
import sys
import os


def hilight(input_string):
    if sys.stdout.isatty():
        # only print escape sequences for TTL interfaces
        return input_string
    attr = []
    attr.append('31')  # red
    attr.append('1')   # bold
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), input_string)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')  # bdist_wininst
    sys.exit()


packages = [
    'dpnewspaper',
]


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='dpnewspaper',
    version='0.25.6',
    description='Customized version from newspaper',
    author='luoyingbo',
    author_email='yingbo@daypop.ai',
    url='http://git.daypop.net/luoyingbo/dpnewspaper',
    packages=packages,
    include_package_data=True,
    install_requires=required,
    license='MIT',
    zip_safe=False,
)

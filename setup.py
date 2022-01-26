import os
import re

from setuptools import setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = [
    'requests',
]


def get_version():
    init = open(os.path.join(ROOT, 'evclient', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='evclient',
    version=get_version(),
    description='NODA EnergyView client API Library',
    long_description=open('README.rst').read(),
    author='NODA Intelligent Systems',
    author_email='mikael.brorsson@noda.se',
    url='https://github.com/noda/evclient',
    scripts=[],
    packages=['evclient'],
    install_requires=requires,
    license='MIT License',
    python_requires='>= 3.7',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)

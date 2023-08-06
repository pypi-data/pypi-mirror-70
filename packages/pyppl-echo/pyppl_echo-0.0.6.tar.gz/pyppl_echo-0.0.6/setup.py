# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_echo']
install_requires = \
['pyppl']

entry_points = \
{'pyppl': ['pyppl_echo = pyppl_echo']}

setup_kwargs = {
    'name': 'pyppl-echo',
    'version': '0.0.6',
    'description': 'Echo script output to PyPPL logs',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

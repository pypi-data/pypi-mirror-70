# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgedl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['pgedl = pgedl.pgedl:run']}

setup_kwargs = {
    'name': 'pgedl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'myyc',
    'author_email': 'myyc@domain.xxx',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

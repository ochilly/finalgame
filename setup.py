try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Game',
    'author': 'chilly',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'chilly.sjn@gmail.com',
    'version': '0.1',
    'install_requires': [''],
    'packages': ['py-txtadv-lpthw'],
    'scripts': [],
    'name': 'py-txtadv-lpthw'
}

setup(**config)

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CSIndexREST',
    version='1.0.0',
    description='CSIndex REST API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/guioliveirabh/CSIndex',
    author='Guilherme Augusto Santos Oliveira',
    author_email='guioliveirabh@gmail.com',
    packages=find_packages(),
    install_requires=['gunicorn==19.8.1', 'Django==2.0.5', 'djangorestframework==3.8.2', 'coreapi==2.3.3',
                      'Markdown==2.6.11', 'django-filter==1.1.0', 'django-crispy-forms==1.7.2',
                      'djangorestframework-csv==2.1.0'],
    extras_require={
        'dev': ['pylint', 'httpie'],
    },
    package_data={},
    entry_points={
        'console_scripts': [
            'csi_server=CSIndexREST.entry_point:entry_point',
        ],
    },
)

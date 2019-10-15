"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jira_database_etl',  # Required
    version='0.0.1',  # Required
    description='Script to import issues from a JIRA instance into a database.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/toddbirchard/jira-database-etl',  # Optional
    author='Todd Birchard',  # Optional
    author_email='toddbirchard@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='JIRA ETL database pipeline data import',  # Optional
    packages=find_packages(),  # Required
    install_requires=['requests', 'pandas', 'sqlalchemy', 'pymysql'],  # Optional
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    entry_points={
        'console_scripts': [
            'main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/toddbirchard/jira-database-etl/issues',
        'Source': 'https://github.com/toddbirchard/jira-database-etl/',
    },
)

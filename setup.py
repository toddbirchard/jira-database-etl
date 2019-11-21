"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jira_database_etl',
    version='1.0.0',
    description='Import JIRA issue data into a SQL database.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/toddbirchard/jira-database-etl',
    author='Todd Birchard',
    author_email='toddbirchard@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='JIRA ETL database pipeline data import',
    packages=find_packages(),
    install_requires=['Requests',
                      'Pandas',
                      'SQLAlchemy',
                      'PyMySQL',
                      'python-dotenv'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    entry_points={
        'console_scripts': [
            'run = main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/toddbirchard/jira-database-etl/issues',
        'Source': 'https://github.com/toddbirchard/jira-database-etl/',
    },
)

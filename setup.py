from setuptools import setup, find_packages
from codecs import open
from os import path

root = path.abspath(path.dirname(__file__))
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-pg-search',
    version='0.0.1',
    description='Django app for making PostgreSQL full text search queries',
    long_description=long_description,
    url='https://github.com/akszydelko/django-pg-search',
    author='Arkadiusz Szydelko',
    author_email='akszydelko@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
    ],
    keywords='django postgresql full text search',
    packages=find_packages(),
    install_requires=['django>=1.8', 'psycopg2>=2.6.1'],
)

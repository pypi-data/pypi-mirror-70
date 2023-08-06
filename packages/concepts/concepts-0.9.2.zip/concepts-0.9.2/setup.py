# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='concepts',
    version='0.9.2',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Formal Concept Analysis with Python',
    keywords='fca complete lattice graph join meet galois',
    license='MIT',
    url='https://github.com/xflr6/concepts',
    project_urls={
        'Documentation': 'https://concepts.readthedocs.io',
        'Changelog': 'https://concepts.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/xflr6/concepts/issues',
    },
    packages=find_packages(),
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'bitsets~=0.7',
        'graphviz~=0.7',
    ],
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=4.6', 'pytest-cov'],
        'docs': ['sphinx>=1.8', 'sphinx-rtd-theme'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

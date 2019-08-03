#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()


requirements = ['colorama', 'GitPython', 'progress']


setup(
        author="0xComposure",
        author_email="0xComposure@gmail.com",
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: Utilities'
        ],
        description='Pull all your git repositories.',
        install_requires=requirements,
        license='MIT',
        long_description_content_type='',
        long_description=readme + "\n\n",
        include_package_data=True,
        keywords="gpullall",
        name="gpullall",
        packages=find_packages(),
        entry_points={
            "console_scripts": ["gpullall = gpullall.__main__:init"]
        },
        setup_requires=requirements,
        url="https://github.com/0xComposure/gpullall",
        version="1.0.0",
        zip_safe=False,
)


from distutils.core import setup

PACKAGE_NAME = 'gpullall'
CLASSIFIERS = [
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
]

setup(
    name=PACKAGE_NAME,
    version='1.0',
    packages=['gpullall'],
    license='MIT',
    long_description=open('README.rst').read(),
    classifiers=CLASSIFIERS
)

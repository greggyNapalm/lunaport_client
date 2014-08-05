import os
import re
from setuptools import setup, find_packages


base_path = os.path.dirname(__file__)
# Get the version (borrowed from SQLAlchemy)
fp = open(os.path.join(base_path, 'lunaport_client', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(fp.read()).group(1)
fp.close()

setup(
    name='lunaport_client',
    version=VERSION,
    author='Gregory Komissarov',
    author_email='gregory.komissarov@gmail.com',
    description='Lunaport REST APIs client',
    long_description='\n' + open('README.rst').read() + '\n\n' + open('CHANGES.rst').read(),
    license='BSD',
    url='https://github.domain/gkomissarov/lunaport_client',
    keywords=['load', 'lunapark', 'api', 'client'],
    packages=[
        'lunaport_client',
    ],
    zip_safe=False,
    install_requires=[
       'requests >= 1.2.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)

"""
This script will work from within the main package directory.
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup
from distutils.util import convert_path
import os, sys

# set package path and name
PACKAGE_PATH = '.'
PACKAGE_NAME = 'pypref'

# check python version
major, minor = sys.version_info[:2]
if major==2 and minor!=7:
    raise RuntimeError("Python version 2.7.x or >=3.x is required.")


# automatically create MANIFEST.in
commands = [# include MANIFEST.in
            '# include this file, to ensure we can recreate source distributions',
            'include MANIFEST.in'
            # exclude all .log files
            '\n# exclude all logs',
            'global-exclude *.log',
            # exclude all other non necessary files
            '\n# exclude all other non necessary files ',
            'global-exclude .project',
            'global-exclude .pydevproject',
            # exclude all of the subversion metadata
            '\n# exclude all of the subversion metadata',
            'global-exclude *.svn*',
            'global-exclude .svn/*',
            'global-exclude *.git*',
            'global-exclude .git/*',
            # include all LICENCE files
            '\n# include all license files found',
            'global-include ./*LICENSE.*',
            # include all README files
            '\n# include all readme files found',
            'global-include ./*README.*',
            'global-include ./*readme.*']
with open('MANIFEST.in','w') as fd:
    for l in commands:
        fd.write(l)
        fd.write('\n')


# declare classifiers
CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Topic :: Software Development
Topic :: Software Development :: Build Tools
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""
# create descriptions
LONG_DESCRIPTION = ["PYthon PREFrences or pypref is a python implementation to creating ",
                    "application's configuration, preferences or settings file and dynamically ",
                    "interacting, updating and pulling them. Most applications have default preferences ",
                    "and in general those are created and stored in a text file (.ini, xml, json, etc). ",
                    "At some point preferences are pulled and updated by the application and/or users. ",
                    "pypref is especially designed to take care of this task automatically and make ",
                    "programming application's preferences more desirable. ",
                    "In addition, pypref allows creating dynamic preferences that will be evaluated real ",
                    "time. This becomes handy in plethora of applications for authentication, automatic ",
                    "key generation, etc. "]
DESCRIPTION      = LONG_DESCRIPTION[:4]


## get package info
PACKAGE_INFO={}
if sys.version_info.major == 2:
    execfile(convert_path( '__pkginfo__.py' ), PACKAGE_INFO)
else:
    exec(open(convert_path( '__pkginfo__.py' )).read(), PACKAGE_INFO)



# create meta data
metadata = dict(name = PACKAGE_NAME,
                packages=[PACKAGE_NAME],
                package_dir={PACKAGE_NAME: '.'},
                version= PACKAGE_INFO['__version__'],
                author="Bachir AOUN",
                author_email="bachir.aoun@e-aoun.com",
                description = ''.join(DESCRIPTION),
                long_description = ''.join(LONG_DESCRIPTION),
                url = "http://bachiraoun.github.io/pypref/",
                download_url = "https://github.com/bachiraoun/pypref",
                license = 'GNU',
                classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
                platforms = ["Windows", "Linux", "Mac OS-X", "Unix"],
                test_suite="tests",
)

# setup
setup(**metadata)

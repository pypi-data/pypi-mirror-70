from setuptools import setup

import glob, os, sys
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

scriptlist = glob.glob(os.path.join('bin', '*.py'))
scriptlist += glob.glob(os.path.join('sbin', '*.py'))

sys.path.insert(0, "src")
from PyFoam import versionString

# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#    long_description = f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyFoam',
    version=versionString(),
    packages=['PyFoam',
                'PyFoam.Applications',
                'PyFoam.Basics',
                'PyFoam.Execution',
                'PyFoam.Infrastructure',
                'PyFoam.Infrastructure.RunHooks',
                'PyFoam.IPythonHelpers',
                'PyFoam.LogAnalysis',
                'PyFoam.RunDictionary',
                'PyFoam.Paraview',
                'PyFoam.Site',
                'PyFoam.ThirdParty',
                'PyFoam.ThirdParty.ply',
                'PyFoam.ThirdParty.Gnuplot',
                'PyFoam.ThirdParty.tqdm',
                'PyFoam.ThirdParty.tqdm.tqdm',
                'PyFoam.Wrappers'],
    #    packages=find_packages('src'),
    package_dir={'':'src'},
    description='Python Utilities for OpenFOAM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://openfoamwiki.net/index.php/Contrib/PyFoam',
    author='Bernhard F.W. Gschaider',
    author_email='bgschaid@hfd-research.com',
    scripts=scriptlist,
    license="GPL",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='cfd openfoam',
    install_requires=['numpy'],
)

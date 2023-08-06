import re
from setuptools import setup, find_packages

long_description = """
A Pure-Python library built as a PDF toolkit.  Prepare documents for distribution.

Features:
- Watermark: Dynamically generate watermarks and add watermark to existing document
- Label: Overlay text labels such as filename or date to documents 
- Encrypt: Password protect and restrict permissions to print only
- Rotate: Rotate by increments of 90 degrees
- Upscale: Scale PDF size
- Merge: Concatenate multiple documents into one file
- Slice: Extract page ranges from documents
- Extract Text and Images
- Retrieve document metadata and information
"""

# Retrieve version number
VERSIONFILE = "pdf/conduit/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    install_requires=[
        'looptools',
        'pdfconduit-convert>=1.2.8',
        'pdfconduit-modify>=2.2.4',
        'pdfconduit-transform>=1.2.2',
        'pdfconduit-utils>=1.1.2',
    ],
    name='pdfconduit',
    version=verstr,
    packages=find_packages(),
    namespace_packages=['pdf'],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)

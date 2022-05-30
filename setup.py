import pathlib
from setuptools import setup

class Version(object):
    name="dbis_btree"
    description="RWTH Aachen Computer Science i5/dbis assets for Lecture Datenbanken und Informationssysteme"
    version='0.0.1'

# The directory containing this file
HERE = pathlib.Path(__file__).parent.resolve()

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dbis-btree",
    version=Version.version,
    description=Version.description,
    long_description=README,
    long_description_content_type="text/markdown",
    author="Lars Leimbach",
    author_email="hochmann@dbis.rwth-aachen.de",
    license="Apache",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=["dbis_btree"],
    include_package_data=True,
    install_requires=[]
)

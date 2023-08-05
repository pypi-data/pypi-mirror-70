from setuptools import setup, find_packages
from gempy import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gempy',
    version=__version__,
    packages=find_packages(exclude=('test', 'docs')),
    include_package_data=True,
    install_requires=[
        'pandas',
        'Theano>=1.0.4',
        'matplotlib',
        'numpy',
        'pytest',
        'seaborn>=0.9',
        'networkx',
        'scikit-image>=0.17',
        'pyvista',
        'iPython',
    ],
    url='https://github.com/cgre-aachen/gempy',
    download_url='https://github.com/cgre-aachen/gempy/archive/2.1.1tar.gz',
    license='LGPL v3',
    author='Miguel de la Varga, Elisa Heim, Alexander Schaaf, Fabian Stamm, Florian Wellmann',
    author_email='varga@aices.rwth-aachen.de',
    description='An Open-source, Python-based 3-D structural geological modeling software.',
    keywords=['geology', '3-D modeling', 'structural geology', 'uncertainty']
)

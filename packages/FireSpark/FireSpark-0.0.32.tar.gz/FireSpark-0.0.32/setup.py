import io
import re

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'description.md'), encoding='utf-8') as f:
    long_description = f.read()

with io.open('FireSpark/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
    if version is None:
        raise ImportError('Could not find __version__ in petastorm/__init__.py')

REQUIRED_PACKAGES = [
	'absl-py>=0.9.0',
    'protobuf>=3.7.1',
	'boto3>=1.5.11',
    's3fs>=0.4.2',
    'urllib3>=1.25.7',
    'numpy>=1.13.3',
    'packaging>=15.0',
    'pandas>=1.0.0',
    'psutil>=4.0.0',
    'pyspark==2.4.5',
    'pyzmq>=14.0.0',
    'pyarrow>=0.12.0',
    'six>=1.5.0',
	'petastorm>=0.8.2',
	'tqdm>=4.43.0',
    'opencv-python>=3.4.3.18',
]

EXTRA_REQUIRE = {
    'opencv': ['opencv-python>=3.4.3.18'],
    'tf': ['tensorflow==1.14.0'],
    'tf_gpu': ['tensorflow-gpu==1.14.0'],
	'tf_datasets': ['tensorflow-datasets>=1.2.0'],
	'imgaug': ['imgaug>=0.4.0'],
    'test': [
        'Pillow>=3.0',
        'codecov>=2.0.15',
        'mock>=2.0.0',
        'opencv-python>=3.4.3.18',
        'flake8',
        'pylint>=1.9',
        'pytest>=3.0.0',
        'pytest-cov>=2.5.1',
        'pytest-forked>=0.2',
        'pytest-logger>=0.4.0',
        'pytest-timeout>=1.3.3',
        's3fs>=0.0.1',
        'gcsfs>=0.2.0',
    ],
    'torch': [
		'torchvision>=0.5.0',
		'torch>=1.2.0',
	],
}

setup(
    name='FireSpark',
    version=version,
    description='FireSpark data processing utility library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://elc-github.magna.global/Magna-Autonomous-Systems/FireSpark',
    author='Hai Yu',
    author_email='hai.yu1@magna.com',
    license='Apache License 2.0',
    classifiers=[
		'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='dataset processing',
    packages=find_packages(exclude=['legacy', 'local_dev', 'mas_datapipe', 'proto_defs', 'tests', 'docs']),
	install_requires=REQUIRED_PACKAGES,
    extras_require=EXTRA_REQUIRE,

)
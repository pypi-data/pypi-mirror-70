from setuptools import find_packages, setup

with open('README.rst') as fp:
    long_description = fp.read()

setup(
    name='schematizer',
    version='0.9.4',
    description='A lightweight library for data marshalling/unmarshalling in Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/eb08a167/schematizer',
    author='Andrew Kiyko',
    author_email='eb08a167@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)

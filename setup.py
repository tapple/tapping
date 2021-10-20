from setuptools import setup, find_packages

setup(
    name='pingdiscover',
    version='0.1.0',
    packages=find_packages(include=['pingdiscover', 'pingdiscover.*']),
    install_requires=[
        'aioping',
    ],
    entry_points={
        'console_scripts': ['pingdiscover=pingdiscover:run_main']
    }
)
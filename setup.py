# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme:
    long_description = ''.join(readme.readlines())

setup(
    name='video_analyzer',
    version='0.2',
    description='Python application for live video stream collection and processing.',
    long_description=long_description,
    author='Aleš Komárek',
    author_email='ales.komarek@newt.cz',
    license='Apache Software License',
    url='http://www.github.cz/cznewt/video-analyzer',
    packages=find_packages(exclude=['.txt']),
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'va_collector = video_analyzer.cli:collector_service',
            'va_processor = video_analyzer.cli:processor_service',
        ],
    },
)

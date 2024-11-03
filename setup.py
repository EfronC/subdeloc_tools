from setuptools import setup, find_packages
import glob

setup(
    name='subdeloc_tools',
    version='0.9.3',
    packages=find_packages(),
    install_requires=[
        "pysubs2",
        "modify-subs"
    ],
    include_package_data=True,
    package_data={
        'subdeloc_tools': ['samples/*.json'],
    },
    author='Efrain Cardenas',  
    author_email='',
    description='Subtitles delocalizer tools.',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EfronC/subdeloc_tools",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',

)
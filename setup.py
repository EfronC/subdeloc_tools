from setuptools import setup, find_packages
import glob

setup(
    name='subdeloc_tools',
<<<<<<< HEAD
    version='0.7.0',
=======
    version='0.8.0',
>>>>>>> 447c026 (few changes)
    packages=find_packages(),
    install_requires=[
        "pysubs2",
        "modify-subs"
    ],
    data_files=[('files', glob.glob('subdeloc_tools/files/**')),],
    author='Efrain Cardenas',  
    author_email='',
    description='Subtitles delocalizer tools.',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EfronC/subdeloc_tools",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',

)
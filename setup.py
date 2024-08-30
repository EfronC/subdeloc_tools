from setuptools import setup, find_packages

setup(
    name='subdeloc_tools',  # Replace with your package’s name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "pysubs2"
    ],
    author='Efrain Cardenas',  
    author_email='',
    description='Subtitles delocalizer tools.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EfronC/subdeloc_tools",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)
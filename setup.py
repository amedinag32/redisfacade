from setuptools import setup, find_packages

setup(
    name='redisfacade',
    version='1.0.1',
    description='A package to implement a facade for accessing Redis databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alan Medina',
    author_email='amedina.escom@hotmail.com',
    url='https://github.com/amedinag32/redisfacade',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'async-timeout==5.0.1',
        'redis==5.2.1'
    ],
)

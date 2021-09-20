from version import __version__
import os
from setuptools import setup

project_name = 'csv2rdf'

setup(
    name=project_name,
    version=__version__,
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='csv2rdf',
    url='',
    author='',
    author_email='',
    license='',
    packages=[project_name],
    install_requires=['pandas', 'click'],
    entry_points={
        'console_scripts': [f'{project_name}={project_name}.command_line:main'],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>= 3.7'
)

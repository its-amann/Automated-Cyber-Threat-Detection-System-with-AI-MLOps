'''
Introduction to setup.py
The setup.py file is used to provide metadata and instructions about your Python project to tools like pip and setuptools. It helps in the following ways:

Package Metadata: Specifies details about the package, such as its name, version, author, license, and description.
Dependencies: Lists the external libraries or dependencies required for the project.
Entry Points: Defines scripts or commands that should be created during the installation.
Package Discovery: Identifies which modules and packages should be included in the distribution.
Distribution: Facilitates the creation of source and binary distributions (e.g., .tar.gz, .whl) for the package.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Function to read the requirements file and return the list of packages
    :return: List of required packages

    """
    requirement_lst:List[str] = []
    try :
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            # Removing the leading/trailing whitespaces
            for line in lines:
                line = line.strip()
                # Ignore the lines which are empty and -e lines
                if line or line != ('-e .'):
                    requirement_lst.append(line)
    except FileNotFoundError:
        print("Requirements file not found")

    return requirement_lst

setup(
    name='Network-Security',
    version='0.0.1',
    author='Aman Agnihotri',
    author_email='amanagnihotri902@gmail.com',
    packages=find_packages(),
    isntall_requires=get_requirements(),
)
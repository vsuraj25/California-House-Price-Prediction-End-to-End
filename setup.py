from setuptools import setup,find_packages
from typing import List


import housing

# Declaring variables for setup function

project_name = "housing-price-predictor"
project_version = '0.0.2'
project_author = "Suraj Verma"
project_description = "This project predicts prices of houses."
requirement_file_name = 'requirements.txt'

def get_requirement_list()->List[str]:
    """
    Description : This function will return list of requirements mentioned
    in the requirements.txt file.

    return: This function will return list of libaries mentioned in the 
    requiremenmts.txt file.

    """
    with open(requirement_file_name) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup(
    name=project_name,
    version = project_version,
    author=project_author,
    description=project_description,
    packages= find_packages(), 
    install_requires = get_requirement_list()
    
    )




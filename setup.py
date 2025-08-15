from setuptools import setup, find_packages
from typing import List

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

def get_requirements(file_path:str) -> List:
    """
    To get all requirement 
    """
    requirements = []
    with open(file_path, "r", encoding="utf-8") as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(
    name="document_portal",
    version="0.1.0",
    author="Muhammed Fayiz",
    author_email="muhammedfayiz122@gmail.com",
    description="RAG project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammedfayiz122/LLMOPS-Tutorials/tree/main/document_portal",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=get_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points={
        "console_scripts": [
            "rag-project=document_portal.app:cli"
        ]
    },
    python_requires='>=3.9',
    license="MIT",
)
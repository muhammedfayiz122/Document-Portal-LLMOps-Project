from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="document_portal",
    version="0.1.0",
    author="Muhammed Fayiz",
    author_email="muhammedfayiz122@gmail.com",
    description="RAG project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammedfayiz122/LLMOPS-Tutorials/tree/main/document_portal",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines() if os.path.exists("requirements.txt") else [],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    license="MIT",
)
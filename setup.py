```python
from setuptools import setup, find_packages

setup(
    name="tvle",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.26.4",
        "matplotlib>=3.9.2",
        "scipy>=1.14.1",
        "tqdm>=4.66.5",
        "ecdsa>=0.19.0",
        "base58>=2.1.1",
    ],
    author="Travis Jones",
    author_email="holedozer@icloud.com",  # Replace with actual email
    description="Temporal Vector Lattice Entanglement Simulation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TravisJones/TVLE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)

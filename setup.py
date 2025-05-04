---

### 3. `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name="tvle",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.23.0",
        "matplotlib>=3.5.0",
        "scipy>=1.8.0",
        "tqdm>=4.64.0",
        "ecdsa>=0.18.0",
        "base58>=2.1.1",
    ],
    author="Travis Jones",
    author_email="travis.jones@example.com",  # Replace with actual email
    description="Temporal Vector Lattice Entanglement Simulation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TravisJones/TVLE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

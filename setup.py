from glob import glob
from setuptools import setup, find_packages

setup(
    name="bike_index_scraper",
    version="0.1.0",
    # about
    author="Thorben Jensen",
    author_email="jensen.thorben@gmail.com",
    description=("Pest monitoring with Raspberry Pi."),
    url="https://github.com/thorbenJensen/pest-pi",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    # code
    packages=find_packages(),
    scripts=glob("scripts/*"),
    # requirementds
    install_requires=[
        "pandas",
        "requests",
        "scikit-learn",
    ],
    extras_require={
        "cpu": ["tensorflow"],
        "gpu": ["tensorflow-gpu"],
        "dev": ["black", "dvc", "dvc[gs]", "flake8", "jupyter", "pylama", "rope"],
    },
)

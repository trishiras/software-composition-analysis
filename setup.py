from setuptools import setup
from software_composition_analysis.__version__ import __version__


setup(
    name="software_composition_analysis",
    version=__version__,
    author="sumit",
    author_email="sumit@mail.com",
    description="software-composition-analysis",
    long_description=open("README.md").read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "software_composition_analysis=software_composition_analysis.main:main",
        ],
    },
)

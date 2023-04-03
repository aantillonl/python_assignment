"""Python setup.py for ctw assignment package"""

from setuptools import find_packages, setup

setup(
    name="ctw_assignment",
    version="0.0.0",
    description="Assignment CTW",
    author="alejandro antillon",
    packages=find_packages(exclude=["tests", ".github"]),
    entry_points={
        "console_scripts": ["get_raw_data = ctw_assignment.get_raw_data:main"]
    },
    extras_require={"test": ["pytest"]},
)
from setuptools import setup, find_packages

setup(
    name="shellex",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "requests>=2.28",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "shellex=shellex.cli:main",
        ],
    },
    python_requires=">=3.9",
)

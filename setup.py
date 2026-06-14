from setuptools import find_packages, setup


setup(
    name="agenttrace",
    version="0.1.0",
    description="Offline analyzer for AI agent execution traces",
    packages=find_packages(include=["agenttrace", "agenttrace.*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "agenttrace=agenttrace.app:main",
        ]
    },
)

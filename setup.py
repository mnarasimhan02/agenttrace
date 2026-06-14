from setuptools import find_packages, setup


setup(
    name="agenttrace",
    version="0.1.0",
    description="Offline analyzer for AI agent execution traces",
    url="https://github.com/mnarasimhan02/agenttrace",
    author="M Narasimhan",
    author_email="mnarasimhan@example.com",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["agenttrace", "agenttrace.*"]),
    include_package_data=True,
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Logging",
    ],
    project_urls={
        "Source": "https://github.com/mnarasimhan02/agenttrace",
    },
    entry_points={
        "console_scripts": [
            "agenttrace=agenttrace.app:main",
        ]
    },
)

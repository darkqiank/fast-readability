from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fast-readability",
    version="0.1.0",
    author="Jiankai Wang",
    author_email="",
    description="A fast HTML content extractor based on Mozilla's Readability.js",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiankaiwang/fast-readability",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.7",
    install_requires=[
        "quickjs",
        "beautifulsoup4",
        "requests",
        "urllib3",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    include_package_data=True,
    package_data={
        "fast_readability": ["js/*.js"],
    },
) 
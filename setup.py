from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="octopus-lightning",
    version="1.0.0",
    author="Octopus AI Solutions",
    author_email="contact@octopus-ai.local",
    description="The Ultra-Fast, Thread-Safe, Sharded In-Memory Cache Client for AI Agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octopus-ai/octopus-lightning",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests>=2.25.1",
    ],
)

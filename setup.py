#!/usr/bin/env python3
"""
Setup per Kimi Guardian
"""

from pathlib import Path

from setuptools import find_packages, setup

# Leggi README
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text() if readme.exists() else ""

setup(
    name="kimi-guardian",
    version="1.0.0",
    author="Kimi Guardian Team",
    author_email="kimi-guardian@example.com",
    description="AI Agent Security Scanner per Kimi Code CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/equacoin/kimi-guardian",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kimi-guardian=guardian.cli:main",
            "kg=guardian.cli:main",  # Shortcut
        ],
    },
    include_package_data=True,
    package_data={
        "guardian": ["config/*.yml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/user/kimi-guardian/issues",
        "Source": "https://github.com/user/kimi-guardian",
    },
)

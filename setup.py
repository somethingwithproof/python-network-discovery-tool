"""
Setup configuration for auto-discover network device management tool.

Requires Python 3.12+
"""

from pathlib import Path

from setuptools import find_packages, setup

version = "0.3.0"

setup(
    name="auto-discover",
    version=version,
    description="A network discovery tool that identifies SSH, SNMP, and MySQL services on network devices",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Typing :: Typed",
    ],
    keywords="network, sysadmin, discovery, snmp, ssh, mysql, scanner",
    author="Thomas Vincent",
    author_email="thomasvincent@gmail.com",
    url="https://github.com/thomasvincent/python-auto-discover-network-Device-Management",
    license="Apache-2.0",
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.12",
    install_requires=[
        "paramiko>=3.5.0",
        "snimpy>=1.1.0",
        "mysqlclient>=2.2.0",
        "openpyxl>=3.1.0",
        "Jinja2>=3.1.0",
    ],
    extras_require={
        "dev": [
            "ruff>=0.5.0",
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
            "mypy>=1.10.0",
            "types-paramiko>=3.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "network-discover=discovery:main",
        ],
    },
)

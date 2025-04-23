"""Setup script for the network-discovery package."""

from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the version from the package
with open(os.path.join("src", "network_discovery", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"

# Define package requirements
requirements = [
    "python-nmap>=0.7.1",
    "redis>=4.0.0",
    "openpyxl>=3.0.0",
    "jinja2>=3.0.0",
    "paramiko>=3.4.0",
    "PyMySQL>=1.0.0",
    "asyncio>=3.4.3",
    "python-libnmap>=0.7.3",
    "ijson>=3.1.4",
]

# Define optional requirements
optional_requirements = {
    "snmp": ["snimpy>=0.8.9"],
    "mysql": ["mysqlclient>=2.0.0"],
}

# Define development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "tox>=4.0.0",
    "twine>=4.0.0",
]

# Define optional dependencies
mysql_requirements = optional_requirements["mysql"]
snmp_requirements = optional_requirements["snmp"]

setup(
    name="network-discovery",
    version=version,
    description="A network discovery tool using Nmap to identify SSH, Ping, SNMP, and MySQL on connected devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thomas Vincent",
    author_email="thomasvincent@gmail.com",
    url="https://github.com/thomasvincent/python-network-discovery-tool/",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    keywords="nmap portscanner network discovery sysadmin",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "mysql": mysql_requirements,
        "snmp": snmp_requirements,
        "all": [req for reqs in optional_requirements.values() for req in reqs],
    },
    entry_points={
        "console_scripts": [
            "network-discovery=network_discovery.interfaces.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

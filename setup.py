from setuptools import setup, find_packages

# Use a constant for the version for easier updates
VERSION = "0.1"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="network-discovery",
    version=VERSION,
    description="A network discovery tool using Nmap to identify SSH, Ping, and SNMP on connected devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Explicitly state it's Markdown
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify Python 3 compatibility
        "Development Status :: 4 - Beta",  # Indicate development status
        "Environment :: Console",  # Specify intended environment
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",  # Use MIT License
        "Operating System :: OS Independent",  # Cross-platform
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    keywords="nmap portscanner network discovery sysadmin",
    author="Thomas Vincent",
    author_email="thomasvincent@gmail.com",
    url="https://github.com/thomasvincent/python-auto-discover",
    license="MIT",  # Use MIT License
    packages=find_packages(exclude=["bnap", "examples", "tests"]),
    include_package_data=True,  # Include non-Python data files
    zip_safe=False,  # May not work within a zip archive if using package data
    install_requires=[
        "python-nmap",  # Assuming you're using this library; add real dependencies
    ],
    entry_points={
        "console_scripts": [
            "auto-discover = auto-discover.main:main"  # CLI command example
        ]
    },
)

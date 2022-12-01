import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="json_linter",
    version="1.0.0",
    entry_points={
        "console_scripts": ["json-linter=json_linter.main:main"],
    },
    author="Christopher Kaster",
    author_email="me@atomicptr.de",
    description="Lint your JSON files!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atomicptr/json-linter",
    packages=setuptools.find_packages(exclude="tests"),
    python_requires=">=3.10",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)

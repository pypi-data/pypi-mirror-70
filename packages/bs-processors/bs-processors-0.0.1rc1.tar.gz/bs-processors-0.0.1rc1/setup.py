import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bs-processors",
    version="0.0.1pre01",
    author="RaduW",
    description="html/xml processors using BeautifulSoup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" https://github.com/RaduW/bs-processors.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

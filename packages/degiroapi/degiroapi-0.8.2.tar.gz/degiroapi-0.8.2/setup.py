import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="degiroapi",
    version="0.8.2",
    author="Lorenz Kraus",
    author_email="lorenz.kraus@gmail.com",
    description="An unofficial API for the trading platform Degiro written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lolokraus/DegiroAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
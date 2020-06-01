import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypkgexp1-skel", # Replace with your desired name
    version="0.0.1",
    author="Sam Zaydel",
    author_email="szaydel@corelight.com",
    description="A skeleton Python package meant to be a pattern for Corelight",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://internal",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "pypkgexp1-cli = pypkgexp1.cli:main_func"
        ],
    },
    test_suite="pypkgexp1.tests.box_test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)

print(f"Packages: {setuptools.find_packages()}")

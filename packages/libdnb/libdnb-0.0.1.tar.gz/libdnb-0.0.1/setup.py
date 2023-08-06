import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libdnb",
    version="0.0.1",
    author="nerrixDE",
    author_email="nerrixde@mailfence.com",
    description="German National library api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nerrixDE/libdnb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)

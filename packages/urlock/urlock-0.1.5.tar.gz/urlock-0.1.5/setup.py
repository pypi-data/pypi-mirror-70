import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urlock", # Replace with your own username
    version="0.1.5",
    author='David Kerschner',
    author_email='dkerschner@gmail.com',
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/baudtack/urlock',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
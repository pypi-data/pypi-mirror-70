import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docstr-md",
    version="0.0.8",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="A fast and easy way to make beautiful documentation markdown files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/docstr-md",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'astor>=0.8.1',
        'pathlib>=1.0.1',
    ]
)
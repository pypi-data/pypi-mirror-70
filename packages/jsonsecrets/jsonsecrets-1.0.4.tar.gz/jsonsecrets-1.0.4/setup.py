import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonsecrets",
    version="1.0.4",
    author="Marco",
    author_email=None,
    description="Load your secrets (API keys etc.) from a JSON file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glowingkitty/JSON-Secrets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["pyprintplus"]
)

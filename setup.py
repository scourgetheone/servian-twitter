import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="servian-twitter-app", # Replace with your own username
    version="0.0.1",
    author="Viet Nguyen",
    author_email="vietnguyen92@hotmail.com",
    description="A small real-time twitter stream web-app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scourgetheone/servian-twitter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)

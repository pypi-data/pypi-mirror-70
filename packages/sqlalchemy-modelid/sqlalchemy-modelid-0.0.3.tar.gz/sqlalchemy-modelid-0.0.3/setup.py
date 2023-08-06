import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-modelid",
    version="0.0.3",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Base with a `model_id` property for SQLAlchemy models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/sqlalchemy-modelid",
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy>=1.3.12',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
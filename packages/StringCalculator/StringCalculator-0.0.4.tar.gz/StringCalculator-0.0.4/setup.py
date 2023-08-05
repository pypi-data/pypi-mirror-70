import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StringCalculator",
    version="0.0.4",
    author="Ido Zahavy",
    author_email="idozahavy@gmail.com",
    description="Calculates string math expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idozahavy/StringCalculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",  # 3 - Alpha , 4 - Beta , 5 - Production/Stable
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
# https://packaging.python.org/tutorials/packaging-projects/

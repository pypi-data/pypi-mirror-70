from setuptools import setup
#from distutils.core import setup

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="kanobu",
    version="0.1.2a1",
    author="Daniel Zakharov",
    author_email="daniel734@bk.ru",
    description="Free implementation of the game \"stone, scissors, paper\"",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="kanobu game",
    url="https://github.com/jDan735/kanobu",
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3",
    install_requires=[
        "colorama",
        "cson"
    ],
    entry_points={
        "console_scripts": [
            "kanobu=kanobu.__main__:main"
        ]
    }
)

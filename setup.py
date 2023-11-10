from setuptools import setup, find_packages

setup(
    name="async-api",
    version="0.1",
    description="An async python backend framework to build fast APIs rapidly.",
    author="Mohamed Naser",
    author_email="mohnas914@email.com",
    url="https://github.com/mn9142001/async-api",
    packages=find_packages(),
    install_requires=[
        "requests-toolbelt==1.0.0"
    ],
)
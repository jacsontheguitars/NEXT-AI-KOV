from setuptools import setup, find_packages

setup(
    name="next-ai-kov",
    version="0.1",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
)

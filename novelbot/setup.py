from setuptools import setup, find_packages

setup(
    name='novelbot',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = novelbot.settings']},
)

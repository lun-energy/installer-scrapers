# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'StoreScraper',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        # 'StoreScraper': ['resources/*.json']
    },
    entry_points = {'scrapy': ['settings = sandbox.settings']
    },
    zip_safe=False,
)
# Automatically created by: shub deploy

from setuptools import setup, find_packages

project_name = 'StoreScraper'
setup(
    name         = project_name,
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        # project_name: ['resources/*.json']
    },
    entry_points = {'scrapy': [f'settings = {project_name}.settings']
    },
    zip_safe=False,
)
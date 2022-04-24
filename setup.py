from setuptools import setup, find_packages

setup(
    name="celery-demo",
    version="1.0.0",
    packages=find_packages(),
    license='',
    # metadata to display on PyPI
    author='Nisheeth Mishra',
    author_email='nmishra2@its.jnj.com',
    description='Demo app for celery usage',
    keywords="<>",
    url="https://jira.jnj.com/projects/ABGN/summary",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://jira.jnj.com/projects/ABGN/summary",
        "Documentation": "https://jira.jnj.com/projects/ABGN/summary",
        "Source Code": "https://jira.jnj.com/projects/ABGN/summary",
    },
    install_requires=[
        'celery',
        'flower'
    ]
)
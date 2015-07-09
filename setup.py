from setuptools import setup, find_packages

version = '0.1'

setup(
    name='decorelate',
    version=version,
    description="",
    long_description="""\
""",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='decorator',
    author='Romain Commandé',
    author_email='commande.romain+decorelate@gmail.com',
    url='http://www.rcomman.de',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    extras_require={
        "develop": [
            "pytest"
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)

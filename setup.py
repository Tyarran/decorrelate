from setuptools import setup, find_packages

version = '0.1'

setup(
    name='decorrelate',
    version=version,
    description="",
    long_description="""\
""",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='decorator',
    author='Romain Commandé',
    author_email='commande.romain+decorrelate@gmail.com',
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

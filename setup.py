from setuptools import setup


setup(
    name='purgedb',
    version='0.0.1',
    entry_points={
        'console_scripts': ['purgedb = purgedb.main:run_app',]
    },
    install_requires=['mysql-connector-python'],
    packages=['purgedb']
)
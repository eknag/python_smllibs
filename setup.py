from setuptools import find_packages, setup
setup(
    name='smllibs',
    packages=find_packages(include=['smllibs']),
    version='0.1.0',
    description='implementing the 15-210 functions in python',
    author='Eknag@andre.cmu.edu',
    license='I don\'t know anything about licensing, but do whatever you want with it!',
    install_requres = [],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
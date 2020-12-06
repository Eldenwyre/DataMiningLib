from setuptools import find_packages, setup

setup(
    name="datamining",
    packages=find_packages(include=["datamining"]),
    version="0.3.2",
    description="",
    author="Eldenwyre",
    license="MIT",
    install_requires=["pandas", "python-dateutil"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.1.2"],
    test_suite="tests",
)

from setuptools import setup, find_packages


__version__ = "0.0.1"
install_requires = [
    "flask"
]


setup(
    name="flask_dashboard",
    version=__version__,
    install_requires=install_requires,
    packages=find_packages()
)
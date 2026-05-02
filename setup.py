from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in intimar_erp/__init__.py
from intimar_erp import __version__ as version

setup(
	name="intimar_erp",
	version=version,
	description="Sistema de gestión y reservas para Intimar",
	author="Intimar",
	author_email="nicole.argueda@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

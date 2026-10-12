from setuptools import setup, find_packages

setup(
    name="erp_fulfillment",
    version="0.1.0",
    description="ERP v1 fulfillment adapters + guards",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

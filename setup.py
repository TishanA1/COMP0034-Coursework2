from setuptools import find_packages, setup

setup(
    name='my_app',
    version='1.0.0',
    packages=["flask_app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalechemy',
        # "pandas",
        # "openpyxl",
        "flask-wtf",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        # "scikit-learn",
    ],
)
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # The line below find the directories (packages) automatically so we do not have to type them out.
    packages=find_packages(),
    # The line below will make the installation includes other folders as templates and static.
    # The additional data that will be installed has to be specified in another doc: MANIFEST.in
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

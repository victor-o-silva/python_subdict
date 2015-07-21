from distutils.core import setup

with open('README.rst', 'r') as readme_file:
    readme_txt = readme_file.read()

with open('LICENSE.txt', 'r') as license_file:
    license_txt = license_file.read()

setup(
    name='subdict',
    packages=['subdict'],
    version='0.5',
    description='Extract subdicts from python dicts by just specifying '
                'which keys are needed, in a dotted-syntax.',
    long_description=readme_txt,
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    license=license_txt,
    url='https://github.com/victor-o-silva/python_subdict',
    download_url='https://github.com/victor-o-silva/python_subdict/tarball/0.5'
)

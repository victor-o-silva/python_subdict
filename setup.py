from distutils.core import setup

readme_file = open('README.md')

setup(
    name='subdict',
    packages=['subdict'],
    version='0.3',
    description='Extract subdicts from python dicts by just specifying '
                'which keys are needed, in a dotted-syntax.',
    long_description=readme_file.read(),
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    url='https://github.com/victor-o-silva/python_subdict',
    download_url='https://github.com/victor-o-silva/python_subdict/tarball/0.3'
)

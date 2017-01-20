from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='puppetbeacon',
    version='0.1.0',
    description='Provides Puppet monitoring capabilities.',
    long_description=readme,
    author='Eric Westfall',
    author_email='eawestfall@gmail.com',
    url='https://github.com/ericwestfall/puppetbeacon',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

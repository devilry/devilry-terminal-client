from setuptools import setup, find_packages

setup(
      name='devilry-terminal-client',
      author=(u'Eskil Opdahl Nordland'),
      author_email='devilry-contact@googlegroups.com',
      url='http://devilry.org',
      description='Library for interacting with devilry REST api and cli',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'setuptools',
          'requests==2.10.0',
      ],
      entry_points={
            'console_scripts': ['devil = devilry.devilcli:main']
      }
)

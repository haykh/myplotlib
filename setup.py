from setuptools import setup

__version__ = '0.1'

setup(
    python_requires='>3.6.0',
    name='myplotlib',
    version=__version__,
    description='`matplotlib` binding with custom styles',
    url='https://github.com/haykh/myplotlib',
    author='Hayk Hakobyan',
    author_email='hayk.hakopyan@gmail.com',
    license='BSD 2-Clause',
    install_requires=[
      'matplotlib>=3.0.0',
      'numpy',
      'tqdm',
      'scipy'
    ],
    packages=['myplotlib'],
    include_package_data=True,
    zip_safe=False
  )

from setuptools import setup, find_packages

__version__ = '0.9.3'

setup(
    python_requires='>3.6.0',
    name='myplotlib',
    version=__version__,
    description='`matplotlib` binding with custom styles',
    url='https://github.com/haykh/myplotlib',
    author='Hayk Hakobyan',
    author_email='haykh.public+myplotlib@gmail.com',
    license='BSD 2-Clause',
    install_requires=[
      'matplotlib>=3.0.0',
      'numpy',
      'tqdm',
      'scipy',
      'numba'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
  )

from setuptools import setup

setup(
    name='myplotlib',
    version='0.1',
    description='`matplotlib` binding with custom styles',
    url='https://github.com/haykh/myplotlib',
    author='Hayk Hakobyan',
    author_email='hayk.hakopyan@gmail.com',
    license='BSD 2-Clause',
    install_requires=[
      'matplotlib',
      'numpy',
      'tqdm',
      'scipy'
    ],
    packages=['myplotlib'],
    package_data={'myplotlib': ['myplotlib/assets/*']},
    include_package_data=True,
    zip_safe=False)


from setuptools import setup, find_packages
#import io

# from distutils.util import convert_path

# main_ns = {}
# ver_path = convert_path('ghost/version.py')
# with open(ver_path) as ver_file:
#     exec(ver_file.read(), main_ns)

# def read(*filenames, **kwargs):
#     encoding = kwargs.get('encoding', 'utf-8')
#     sep = kwargs.get('sep', '\n')
#     buf = []
#     for filename in filenames:
#         with io.open(filename, encoding=encoding) as f:
#             buf.append(f.read())
#     return sep.join(buf)

# long_description = read('README.rst')

setup(
    name='ghostipy',
    version='0.0.2',
    license='Apache License',
    author='Joshua Chu',
    install_requires=['numpy>=1.18.1',
                      'scipy>=1.4.1',
                      'pyfftw>=0.12.0',
                      'numba>=0.48.0',
                      'dask>=2.15.0',
                      'xarray>=0.15.1',
                      'matplotlib>=3.1.3',
                      'datashader>=0.10.0',
                      'hvplot>=0.5.2'
                     ],
    author_email='jpc6@rice.edu',
    description='Signal processing and spectral analysis toolbox',
    packages=find_packages(),
    keywords="neuroscience spectral analysis",
    include_package_data=True,
    platforms='any'
)

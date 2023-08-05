# from distutils.core import setup
from setuptools import setup

setup(
    name='pyunsplash',
    version='1.0.0rc2',  # beta, v9
    packages=['pyunsplash', 'pyunsplash.src'],
    url='https://github.com/salvoventura/pyunsplash',
    license='MIT',
    author='salvatore ventura',
    author_email='salvoventura@gmail.com',
    description='A Python wrapper for the Unsplash.com REST API',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords=['unsplash', 'rest', 'api', 'python', 'wrapper', 'development', 'unsplash.com', 'photography'],
    install_requires=['requests'],
    python_requires='>=2.7'
)


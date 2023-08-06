from distutils.core import setup
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'margot',
    packages = ['margot'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='apache-2.0',
    description = 'simple to use, batteries included, tools for quantitative trading.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = 'Rich Atkinson',
    author_email = 'rich@airteam.com.au',
    url = 'https://github.com/atkinson/margot',
    download_url = 'https://github.com/atkinson/margot/archive/v_0.1-alpha.tar.gz',
    keywords = ['quant', 'trading', 'systematic'],
    install_requires=[
            'numpy',
            'pandas',
            'scipy',
            'pyfolio',
            'trading-calendars'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
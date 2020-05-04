from setuptools import setup

setup(
    url              = 'https://github.com/TheMrinalSinha/tmsutils',
    name             = 'tmsutils',
    author           = 'Mrinal Sinha',
    version          = '1.0.6',
    packages         = ['tmsutils'],
    py_modules       = ['tmsutils'],
    description      = 'Handy tools out of the box',
    author_email     = 'mail@themrinalsinha.com',
    install_requires = [pkg for pkg in open('requirements.txt').read().split('\n') if pkg],
    classifiers      = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",

    entry_points = '''
        [console_scripts]
        tms=tmsutils:cli
    '''
)

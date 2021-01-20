from setuptools import setup

setup(
    name='SnusBrute',
    version='0.1.0',
    author='Haviv Vaizman',
    author_email='Havivv1305@gmail.com',
    license='LICENSE',
    py_modules=['SnusBrute'],
    description='Get all leaks of ur organization from SnusBase.',
    entry_points={
        'console_scripts': [
                'snusbrute=SnusBase:SnusBaseBrute',
        ],
    },
    install_requires=[
        "click==6.7",
        "colorlog",
        "bs4==0.0.1"

    ]
)

from setuptools import setup

setup(
    name='temser',
    version='0.1.0',
    description='A templating engine and web server for data driven pages.',
    url='https://github.com/dagnelies/temser',
    author='Arnaud Dagnelies',
    author_email='arnaud.dagnelies@gmail.com',
    license='MIT',
    keywords='template server',
    py_modules=['temser'],
    scripts=['temser.py'],
    install_requires=[
        'bottle',
        'pystache'
    ]
)
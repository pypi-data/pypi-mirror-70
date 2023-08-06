"""Setup.py for the expansion package."""

import setuptools

with open('README.rst', 'r') as read_me:
    README = read_me.read()

setuptools.setup(
    name='expansion-raj-csh',
    version='1.0.2',
    author='Rajarshi Mandal',
    author_email='rajarshimandal22@gmail.com',
    description='A simple generative art project.',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/Raj-CSH/expansion',
    packages=setuptools.find_packages(),
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'],
    install_requires=['numpy',
                      'opencv-python',
                      'pillow',
                      'pygame'],
    python_requires='>=3.6'
)

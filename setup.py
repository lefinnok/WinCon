from setuptools import setup, find_packages

setup(
    name='WinCon',
    packages=find_packages(),
    version='0.1',
    description='A Windows Console ASCII Graphics Module',
    licence='GNU Affero General Public License v3.0',
    author='Chak Lai KWOK',
    author_email='lefinnokwok@gmail.com',
    url='https://github.com/lefinnok/WinCon',
    keywords=['console', 'graphics', 'ASCII'],  # arbitrary keywords
    install_requires=[
        'pytest>=2.9.2',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3.0 ',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)

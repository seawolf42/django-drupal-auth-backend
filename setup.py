import os
from setuptools import find_packages, setup


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
        README = readme.read()
except Exception:
    README = '<failed to open README.rst>'


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


install_dependencies = (
    'Django>=1.8',
)


setup(
    name='django-drupal-password-hasher',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3 or later (GPLv3+)',
    description='Password hasher for Django that works with legacy Drupal 7 accounts.',
    long_description=README,
    url='https://github.com/seawolf42/django-drupal-password-hasher',
    author='jeffrey k eliasen',
    author_email='jeff+django-drupal-password-hasher@jke.net',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    keywords='',
    install_requires=install_dependencies,
    tests_require=install_dependencies + ('mock',),
)
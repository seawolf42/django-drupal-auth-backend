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
    name='django-drupal-auth-backend',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3 or later (GPLv3+)',
    description='Authentication backend for Django that works with legacy Drupal 7 accounts.',
    long_description=README,
    url='https://github.com/seawolf42/django-drupal-auth-backend',
    author='jeffrey k eliasen',
    author_email='jeff+django-drupal-auth-backend@jke.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    keywords='django-drupal-auth-backend',
    install_requires=install_dependencies,
    tests_require=install_dependencies + ('mock',),
)

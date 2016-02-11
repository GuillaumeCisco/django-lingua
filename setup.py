from setuptools import setup, find_packages

setup(
    name='lingua',
    version='0.9.0',
    url='http://github.com/geomin/django-lingua',
    maintainer='Guillaume Cisco',
    maintainer_email='guillaumecisco@gmail.com',
    description='Django model translation on basis of gettext',
    classifiers=['License :: OSI Approved :: BSD License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: I18N :: Internalization'],
    license='BSD',
    platforms=['any'],
    install_requires=['polib'],#pip
    packages=find_packages(),
)

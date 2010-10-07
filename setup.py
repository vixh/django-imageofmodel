from setuptools import setup, find_packages

setup(
    name='django-imagheofmodel',
    version=__import__('imagheofmodel').__version__,
    description='Holds Image of Model for Django',
    #long_description=open('docs/overview.txt').read(),
    author='Viktor Shulika',
    author_email='ya.vixh@ya.ru',
    url='http://github.com/vixh/django-imageofmodel',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        'robots': [
        ],
    },
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ]
)

from setuptools import setup

setup(name='keycloak_wrapper',
      version='0.2',
      description='A python wrapper for keycloak',
      url='https://github.com/kapsali29/keycloak_wrapper',
      author='Panagiotis Kapsalis',
      author_email='kapsali29@gmail.com',
      license='MIT',
      packages=['keycloak_wrapper'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
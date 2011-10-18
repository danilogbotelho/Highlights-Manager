from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.highlights.manager',
      version=version,
      description="Provides a plonish way of managing featured content",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='highlight featured content manager lead',
      author='Danilo G. Botelho',
      author_email='danilogbotelho@yahoo.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.highlights'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
      ],
      extras_require={
          'test': ['plone.app.testing',],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

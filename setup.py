from setuptools import setup, find_packages

setup(name='sikwidgets',
      version='0.1.0',
      description='Adds GUI mockup functionality to Sikuli for easier, robust testing',
      author='Joel Griffith',
      packages=find_packages(),
      scripts=['bin/sikwidgets_script.py', 'bin/sikwidgets.bat', 'bin/sikwidgets']
)
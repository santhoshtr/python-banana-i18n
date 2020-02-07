from setuptools import setup

setup(
    name='banana-i18n',
    version='0.1.3',
    packages=['banana_i18n'],
    package_data={'banana_i18n': ['py.typed']},
    python_requires='>=3.5',
    url='https://git.legoktm.com/legoktm/banana-i18n',
    include_package_data=True,
    license='MIT',
    author='Kunal Mehta',
    author_email='legoktm@member.fsf.org',
    long_description=open('README.rst').read(),
    description='An i18n library based on the banana message format'
)

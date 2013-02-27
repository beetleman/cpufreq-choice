from setuptools import setup

setup(
    name='Cpufreq-choice',
    version='0.1',
    url='https://bitbucket.org/robal/cpufreq-choice',
    description='CLI curses-based cputoold',
    author='Mateusz Probachta aka robal',
    author_email='nigrantis.tigris@gmail.com',
    license="LGPL",
    keywords="cli curses cpu system",
    long_description=open('README').read(),
    install_requires=['urwid'],
    packages=['cpufreqc',
              'cpufreqc.libs'],
    include_package_data=True,
    entry_points={"console_scripts": ["cpufreqc-tui=cpufreqc.cpufreqc_tui:main"]},
)

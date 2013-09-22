from setuptools import setup

setup(
    name='Cpufreq-choice',
    version='0.2',
    url='https://github.com/beetleman/cpufreq-choice',
    description='CLI curses-based cputool',
    author='Mateusz Probachta aka beetleman',
    author_email='nigrantis.tigris@gmail.com',
    license="LGPL",
    keywords="cli curses cpu system",
    long_description=open('README').read(),
    install_requires=['urwid'],
    packages=['cpufreqc',
              'cpufreqc.libs'],
    include_package_data=True,
    platforms='Linux',
    entry_points={"console_scripts": ["cpufreqc-tui=cpufreqc.cpufreqc_tui:main"]},
)

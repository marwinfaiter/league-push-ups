import os
from setuptools import setup, find_packages

PKG = 'league-push-ups'
######
setup(
    name=PKG,
    version=f"0.0.{os.environ.get('BUILD_ID', 1)}",
    description='Simple pyplanet application to add random map game modes online',
    long_description='',
    keywords='LoL Push-ups',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(include=["league_push_ups.*"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    package_data={},
    author='marwinfaiter',
    author_email='noobgubbe@gmail.com',
    url='https://github.com/marwinfaiter/league-push-ups',
    classifiers=[  # Please update this. Possibilities: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

        'Operating System :: OS Independent',

        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',

    ],
    # entry_points = {
    #     'console_scripts': [
    #         'league-push-ups = league_push_ups.__main__:main',
    #     ],
    # },
    zip_safe=False,
    install_requires=[
        "discord",
        "lcu_driver",
        "requests",
    ],
    extras_require={
        "test": [
            "mypy",
            "pytest",
            "pylint",
            "mockito"
        ]
    }
)

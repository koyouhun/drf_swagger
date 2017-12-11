from distutils.core import setup

setup(
    name='drf_swagger',
    version='0.1.0',
    packages=['drf_swagger'],
    url='https://github.com/koyouhun/drf_swagger',
    download_url='https://github.com/koyouhun/drf_swagger/archive/0.1.0.tar.gz',
    license='BSD',
    author='YouHyeon Ko',
    author_email='koyouhun@gmail.com',
    description='Django REST Framework + Swagger',
    keywords=['django', 'swagger', 'api', 'documentation'],
    classifiers=[
          'License :: BSD',
          'Programming Language :: Python :: 2.7'
      ],
    install_requires=[
        'Django>=1.7',
        'PyYAML>=3.12',
        'six>=1.10.0',
        'uritemplate>=3.0.0',
        'djangorestframework>=3.6.0'
    ]
)

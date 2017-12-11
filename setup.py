from setuptools import setup, find_packages

setup(
    name='drf_swagger',
    version='0.1.2',
    packages=find_packages(),
    package_data={
        '': ['README.md'],
        'drf_swagger': ['static/favicon-16x16.png',
                        'static/favicon-32x32.png',
                        'static/swagger-ui-bundle.js',
                        'static/swagger-ui-bundle.js.map',
                        'static/swagger-ui-standalone-preset.js',
                        'static/swagger-ui-standalone-preset.js.map',
                        'static/swagger-ui.css',
                        'static/swagger-ui.css.map',
                        'static/swagger-ui.js',
                        'static/swagger-ui.js.map',
                        'templates/index.html',
                        'templates/oauth2-redirect.html'],
    },
    url='https://github.com/koyouhun/drf_swagger',
    license='BSD',
    author='YouHyeon Ko',
    author_email='koyouhun@gmail.com',
    description='Django REST Framework + Swagger',
    keywords=['django', 'swagger', 'api', 'documentation'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7'
      ],
    install_requires=[
        'Django<=1.11',
        'PyYAML',
        'six',
        'uritemplate',
        'djangorestframework>=3.6.0'
    ]
)

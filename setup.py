from setuptools import find_packages, setup

setup(
    name='www_eaveson_co_uk',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'click',
        'Flask',
        'Flask-SQLAlchemy',
        'gitdb',
        'GitPython',
        'itsdangerous',
        'Jinja2',
        'Markdown',
        'MarkupSafe',
        'Pygments',
        'python-dotenv',
        'smmap',
        'SQLAlchemy',
        'Werkzeug',
    ],
)
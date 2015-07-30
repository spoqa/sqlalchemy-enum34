import ast
import os.path
import sys

from setuptools import setup


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


def get_version():
    module_path = os.path.join(os.path.dirname(__file__),
                               'sqlalchemy_enum34.py')
    module_file = open(module_path)
    try:
        module_code = module_file.read()
    finally:
        module_file.close()
    tree = ast.parse(module_code, module_path)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, = node.targets
        if isinstance(target, ast.Name) and target.id == '__version__':
            return node.value.s


def get_install_requires():
    install_requires = ['setuptools', 'SQLAlchemy >= 0.8.0']
    if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 4):
        install_requires.append('enum34')
    return install_requires


def get_extras_require():
    """Generate conditional requirements with environ marker."""
    for pyversion in '2.5', '2.6', '2.7', '3.2', '3.3':
        yield ':python_version==' + repr(pyversion), ['enum34']


setup(
    name='SQLAlchemy-Enum34',
    description='SQLAlchemy type to store standard enum.Enum value',
    long_description=readme(),
    version=get_version(),
    url='https://github.com/spoqa/sqlalchemy-enum34',
    author='Hong Minhee',
    author_email='hongminhee' '@' 'member.fsf.org',
    license='MIT License',
    py_modules=['sqlalchemy_enum34'],
    install_requires=get_install_requires(),
    extras_require=dict(get_extras_require()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Programming Language :: SQL',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
    ]
)

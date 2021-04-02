import ast
import os.path
import sys

from setuptools import setup


def readme():
    try:
        with open('README.rst') as f:
            readme = f.read()
    except IOError:
        pass
    try:
        with open('CHANGES.rst') as f:
            readme += '\n\n' + f.read()
    except IOError:
        pass
    return readme


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
    setup_requires=[
        'setuptools~=44.1.0; python_version<"3"',
        'setuptools>=54.2.0; python_version>="3"',
        'wheel>=0.36.2',
    ],
    install_requires=[
        'SQLAlchemy>=1.3.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Programming Language :: SQL',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
    ]
)

SQLAlchemy-Enum34
=================

.. image:: https://badge.fury.io/py/SQLAlchemy-Enum34.svg?
   :target: https://pypi.python.org/pypi/SQLAlchemy-Enum34
.. image:: https://travis-ci.org/spoqa/sqlalchemy-enum34.svg?branch=master
   :target: https://travis-ci.org/spoqa/sqlalchemy-enum34
.. image:: https://codecov.io/github/spoqa/sqlalchemy-enum34/coverage.svg?branch=master
   :target: https://codecov.io/github/spoqa/sqlalchemy-enum34?branch=master

This package provides a SQLAlchemy type to store values of standard
``enum.Enum`` (which became a part of standard library since Python 3.4).
Its internal representation is equivalent to SQLAlchemy's built-in
``sqlalchemy.types.Enum``, but its Python representation is not
a ``str`` but ``enum.Enum``.

Note that this works on Python 2.6 as well as 3.4, the latest version of
Python, through enum34_ package.

The following example shows how enum_-typed columns can be declared::

    import enum

    from sqlalchemy import Column, Integer
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy_enum34 import EnumType

    Base = declarative_base()

    class Color(enum.Enum):
        black = 'black'
        white = 'white'
        navy = 'navy'
        red = 'red'

    class Size(enum.Enum):
        small = 'S'
        medium = 'M'
        large = 'L'
        xlarge = 'XL'

    class Shirt(Base):
        id = Column(Integer, primary_key=True)
        color = Column(EnumType(Color), nullable=False)
        size = Column(EnumType(Size, name='shirt_size'), nullable=False)

And the following REPL session shows how these columns work:

>>> shirt = session.query(Shirt).filter(Shirt.color == Color.navy).first()
>>> shirt.color
<Color.navy: 'navy'>
>>> shirt.size
<Size.large: 'large'>

Written by `Hong Minhee`_ at Spoqa_, and distributed under MIT license.

.. _enum34: https://pypi.python.org/pypi/enum34
.. _enum: https://docs.python.org/3/library/enum.html
.. _Hong Minhee: http://hongminhee.org/
.. _Spoqa: http://www.spoqa.com/

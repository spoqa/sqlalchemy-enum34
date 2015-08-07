""":mod:`sqlalchemy_enum34` --- SQLAlchemy :class:`enum` type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import enum

from sqlalchemy.types import Enum as BaseEnum, SchemaType, TypeDecorator

__all__ = 'Enum', 'EnumType'
__version__ = '1.0.1'


class Enum(TypeDecorator, SchemaType):
    """Store values of standard :class:`enum.Enum` (which became a part of
    standard library since Python 3.4).
    Its internal representation is equivalent to SQLAlchemy's built-in
    :class:`~sqlalchemy.types.Enum`, but its Python representation is not
    a :class:`str` but :class:`enum.Enum`.

    :param enum_class: the :class:`enum.Enum` subclass
    :type enum_class: :class:`type`
    :param by_name: whether to store values by its name instead of its value.
                    :const:`False` by default
    :type by_name: :class:`bool`
    :param \*\*options: rest keyword arguments will be passed to
                        :class:`~sqlalchemy.types.Enum` constructor

    """

    impl = BaseEnum

    def __init__(self, enum_class, by_name=False, **options):
        if not issubclass(enum_class, enum.Enum):
            raise TypeError('expected enum.Enum subtype')
        if by_name:
            enumerants = [m.name for m in enum_class]
        else:
            enumerants = [m.value for m in enum_class]
        super(Enum, self).__init__(*enumerants, **options)
        self._enum_class = enum_class
        self._by_name = bool(by_name)

    def process_bind_param(self, value, dialect):
        if self._by_name:
            return value.name if value else None
        return value.value if value else None

    def process_result_value(self, value, dialect):
        if self._by_name:
            return self._enum_class[value] if value else None
        return self._enum_class(value) if value else None

    def _set_parent(self, column):
        self.impl._set_parent(column)

    @property
    def python_type(self):
        return self._enum_class


#: Alias of :class:`Enum`.  Can used for disambiguating from
#: :class:`enum.Enum` when their names get duplicated.
EnumType = Enum

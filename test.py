import enum
import os

from pytest import fixture, yield_fixture
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

from sqlalchemy_enum34 import Enum, EnumType


Base = declarative_base()
Session = sessionmaker()


class Color(enum.Enum):

    red = 'r'
    green = 'g'
    blue = 'b'


class ColorTable(Base):

    id = Column(Integer, primary_key=True)
    color_by_val = Column(Enum(Color, name='color_by_val'))
    color_by_name = Column(Enum(Color, by_name=True, name='color_by_name'))

    __tablename__ = 'tb_color'


try:
    database_urls = os.environ['TEST_DATABASE_URLS'].split()
except KeyError:
    database_urls = []


@fixture(scope='function', params=['sqlite://'] + database_urls)
def fx_engine(request):
    url = request.param
    engine = create_engine(url, poolclass=NullPool)
    request.addfinalizer(engine.dispose)
    return engine


@yield_fixture
def fx_connection(fx_engine):
    connection = fx_engine.connect()
    try:
        transaction = connection.begin()
        try:
            metadata = Base.metadata
            metadata.create_all(bind=connection)
            yield connection
        finally:
            transaction.rollback()
    finally:
        connection.close()


@yield_fixture
def fx_session(fx_connection):
    session = Session(bind=fx_connection)
    try:
        yield session
    finally:
        session.close()


@fixture
def fx_red(fx_session):
    red = ColorTable(color_by_val=Color.red, color_by_name=Color.red)
    fx_session.add(red)
    fx_session.flush()
    return red


@fixture
def fx_green(fx_session):
    green = ColorTable(color_by_val=Color.green, color_by_name=Color.green)
    fx_session.add(green)
    fx_session.flush()
    return green


@fixture
def fx_blue(fx_session):
    blue = ColorTable(color_by_val=Color.blue, color_by_name=Color.blue)
    fx_session.add(blue)
    fx_session.flush()
    return blue


def test_enum_by_value(fx_session, fx_blue, fx_red):
    result = fx_session.query(ColorTable) \
                       .filter_by(color_by_val=Color.blue) \
                       .one()
    assert fx_blue is result
    result2 = fx_session.query(ColorTable) \
                        .filter("tb_color.color_by_val = 'r'") \
                        .one()
    assert fx_red is result2


def test_enum_by_name(fx_session, fx_green, fx_blue):
    result = fx_session.query(ColorTable) \
                       .filter_by(color_by_name=Color.green) \
                       .one()
    assert fx_green is result
    result2 = fx_session.query(ColorTable) \
                        .filter("tb_color.color_by_name = 'blue'") \
                        .one()
    assert fx_blue is result2


def test_enum_is_enum_type():
    assert Enum is EnumType

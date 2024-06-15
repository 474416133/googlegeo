#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：babikill -> models
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/6/15 21:44
@Desc   ：
"""
import collections
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import attributes


def to_dict(model, field_names=None):
    """
    model to dict
    :param model:
    :return:
    """
    if not model:
        return None
    model_cls = model.__class__
    if field_names is None:
        field_names = [c for c in model.__dict__ if isinstance(getattr(model_cls, c, None), attributes.InstrumentedAttribute)]
    elif not isinstance(field_names, (collections.Iterable, collections.Iterator)):
        raise RuntimeError('columns must be either Iterable or Iterator')
    return dict((c, model.__dict__.get(c, None)) for c in field_names)


class Base(DeclarativeBase):
    pass



class Company(Base):

    __tablename__ = 'company'

    id:            Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:          Mapped[str] = mapped_column(String(200))
    degree:        Mapped[str] = mapped_column(String(100))
    cat:           Mapped[str] = mapped_column(String(100))
    address:       Mapped[str] = mapped_column(String(300))
    open_status:   Mapped[str] = mapped_column(String(50))
    open_time:     Mapped[str] = mapped_column(String(100))
    contact:       Mapped[str] = mapped_column(String(20))
    web_site:      Mapped[str] = mapped_column(String(300))



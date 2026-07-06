#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2026-07-06 13:49:50
# @Author  : xxyyzz
# @Link    : page
# @Version : 0.0.1
# @Desc    : 分页
from typing import Generic, List, TypeVar

from main.base.camel_case_model import CamelCaseModel

T = TypeVar('T')

class Page(CamelCaseModel, Generic[T]):
    items: List[T]
    total: int
    page_no: int
    size: int
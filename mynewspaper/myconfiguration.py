#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/4/18 15:30
# Desc    :   

from newspaper.configuration import (
    Configuration
)

from .myparsers import (
    MYParse
)


class MYConfiguration(Configuration):
    def __init__(self):
        super(MYConfiguration, self).__init__()

    def get_parser(self):
        return MYParse

    pass

#!/usr/bin/env python
#-*- encoding: utf-8 -*-
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

from .dpparsers import (
    DPParse
)


class DPConfiguration(Configuration):
    def __init__(self):

        super(DPConfiguration, self).__init__()

    def get_parser(self):
        return DPParse
    pass

#!/usr/bin/env python3
# coding: utf-8

__version__ = '0.4.2'

from joker.broker.access import ResourceBroker


def get_resource_broker(path=None):
    from joker.broker.default import default_conf_path
    return ResourceBroker.create(path or default_conf_path)

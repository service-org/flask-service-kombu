#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from flask import Flask
from service_kombu.core.publish import Publisher
from service_kombu.constants import KOMBU_CONFIG_KEY
from service_kombu.core.standalone.amqp.rpc import AMQPRpcRequest
from service_kombu.core.standalone.amqp.pub import AMQPPubStandaloneProxy
from service_kombu.core.standalone.amqp.rpc import AMQPRpcStandaloneProxy


class ServiceKombu(object):
    """ ServiceKombu插件配置 """

    amqp = {'pub': None, 'rpc': None}

    def __init__(self, app: t.Optional[Flask] = None) -> None:
        """ 初始化实例

        @param app: 应用对象
        """
        self.app = app
        self.app and self.init_app(app)

    def init_app(self, app: t.Optional[Flask] = None) -> None:
        """ 初始化应用

        @param app: 应用对象
        @return: None
        """
        app.config.setdefault(KOMBU_CONFIG_KEY, {})

    @property
    def amqp_pub(self) -> Publisher:
        """ 获取AMQP PUB代理 """
        config = self.app.config.get(KOMBU_CONFIG_KEY, {})
        if self.amqp['pub'] is None:
            proxy = AMQPPubStandaloneProxy(config=config)
            self.amqp['pub'] = proxy.as_inst()  # type: ignore
        return self.amqp['pub']  # type: ignore

    @property
    def amqp_rpc(self) -> AMQPRpcRequest:
        """ 获取AMQP RPC代理 """
        config = self.app.config.get(KOMBU_CONFIG_KEY, {})
        if self.amqp['rpc'] is None:
            proxy = AMQPRpcStandaloneProxy(config=config,
                                           drain_events_timeout=None)
            self.amqp['rpc'] = proxy.as_inst()  # type: ignore
        return self.amqp['rpc']  # type: ignore

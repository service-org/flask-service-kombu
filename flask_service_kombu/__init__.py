#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from flask import Flask
from service_kombu.constants import KOMBU_CONFIG_KEY
from service_kombu.core.standalone.amqp.pub import AMQPPubStandaloneProxy
from service_kombu.core.standalone.amqp.rpc import AMQPRpcStandaloneProxy


class ServiceKombu(object):
    """ ServiceKombu插件配置 """

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

    def get_amqp_rpc_proxy(self) -> AMQPRpcStandaloneProxy:
        """ 获取AMQP RPC请求代理 """
        config = self.app.config.get(KOMBU_CONFIG_KEY, {})
        return AMQPRpcStandaloneProxy(config=config)

    def get_amqp_pub_proxy(self) -> AMQPPubStandaloneProxy:
        """ 获取AMQP PUB请求代理 """
        config = self.app.config.get(KOMBU_CONFIG_KEY, {})
        return AMQPPubStandaloneProxy(config=config)

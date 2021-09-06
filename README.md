# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U django-service-kombu
```

# 入门案例

```yaml
├── manage.py
└── project
    ├── __init__.py
    ├── asgi.py
    ├── urls.py
    ├── wsgi.py
    └── settings.py
```

> settings.py

```python
INSTALLED_APPS = [
    # 主要用于配置检查,可不配置
    'flask_service_kombu',
]

KOMBU = {
    'connect_options': {
        'hostname': 'pyamqp://admin:nimda@127.0.0.1:5672//'
    },
    'consume_options': {
        
    },
    'publish_options': {
        
    }
}
```

> urls.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import json

from kombu import Exchange
from django.urls import path
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from flask_service_kombu.proxy import get_amqp_pub_proxy
from flask_service_kombu.proxy import get_amqp_rpc_proxy


def test_amqp_pub(request: HttpRequest) -> HttpResponse:
    """ 测试AMQP PUB请求

    @param request: 请求对象
    @return: HttpResponse
    """
    with get_amqp_pub_proxy() as pub:
        publish_options = {'exchange': Exchange('demo'),
                           'routing_key': 'demo.test_amqp_rpc'}
        pub.publish('from django test_amqp_pub', **publish_options)
    return HttpResponse('succ')


def test_amqp_rpc(request: HttpRequest) -> HttpResponse:
    """ 测试AMQP RPC请求

    @param request: 请求对象
    @return: HttpResponse
    """
    with get_amqp_rpc_proxy() as rpc:
        body, message = rpc.send_request('demo.test_amqp_rpc', {}).result
    data = json.dumps(body)
    return HttpResponse(data)


urlpatterns = [
    path('test-amqp-pub/', test_amqp_pub, name='test-amqp-pub'),
    path('test-amqp-rpc/', test_amqp_rpc, name='test-amqp-rpc'),
]
```

# 运行服务

> python3 manage.py runserver -v 3 --traceback --force-color

# 接口测试

```bash
curl http://127.0.0.1:8000/test-amqp-pub/

curl http://127.0.0.1:8000/test-amqp-rpc/
```


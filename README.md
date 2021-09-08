# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U flask-service-kombu
```

# 入门案例

```yaml
└── project
    ├── __init__.py
    └── service.py
```

> service.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from flask import Flask
from flask import jsonify
from kombu import Exchange
from flask import Response
from flask_service_kombu import ServiceKombu
from service_kombu.constants import KOMBU_CONFIG_KEY

app = Flask(__name__)
app.config.from_mapping({
    KOMBU_CONFIG_KEY: {
        'connect_options': {
            'hostname': 'pyamqp://admin:nimda@127.0.0.1:5672//'
        },
        'consume_options': {

        },
        'publish_options': {

        }
    }
})
service_kombu = ServiceKombu(app)


@app.route('/test-amqp-rpc/')
def test_amqp_rpc() -> Response:
    """ 测试AMQP RPC请求 """
    body, message = service_kombu.amqp_rpc.send_request('demo.test_amqp_rpc', {}).result
    return jsonify(body)


@app.route('/test-amqp-pub/')
def test_amqp_pub() -> Response:
    """ 测试AMQP PUB请求 """
    publish_options = {'exchange': Exchange('demo'), 'routing_key': 'demo.test_amqp_rpc'}
    service_kombu.amqp_pub.publish('from flask test_amqp_pub', **publish_options)
    return Response('publish succ')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
```

# 运行服务

> python3 service.py

# 优化建议

> uwsgi驱动时请设置`lazy-apps = true`和`enable-threads = true`

# 接口测试

```bash
curl http://127.0.0.1:8000/test-amqp-pub/

curl http://127.0.0.1:8000/test-amqp-rpc/
```

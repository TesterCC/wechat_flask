# coding:utf-8

"""
不设置FLASK_APP
terminal虚拟环境下直接运行python wechat.py
也能启动app
"""

import hashlib
from flask import Flask, request, abort

# 常量放这里
# wechat token
WECHAT_TOKEN = "aictftmp"  # config by yourself

app = Flask(__name__)


@app.route('/wechat')
def wechat():
    """
    对接微信公众号服务器
    """
    # receive wechat server send args
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    # 校验参数
    if not all([signature, timestamp, nonce, echostr]):
        abort(400)

    # 按照微信的流程进行计算签名
    li = [WECHAT_TOKEN, timestamp, nonce]
    # 按字典序排序
    li.sort()
    # cat str
    tmp_str = "".join(li)
    # Encrypt with SHA1, get correct signature value
    sign = hashlib.sha1(tmp_str).hexdigest()

    # 将自己计算的签名值与请求的签名参数进行对比，若相同，则证明请求来自微信
    if signature != sign:
        abort(403)  # 表示请求来源不是微信
    else:
        return echostr


@app.route('/')
def index():
    return '<h1>Server works on ...</h1>'


if __name__ == '__main__':
    app.run(port=8888, debug=True)

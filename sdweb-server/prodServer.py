from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from flask import Flask, request, redirect
from api.stablediffusion import app
from config.setting import SSL_CA_FILE,SSL_CA_KEY_FILE,SERVER_PORT,SSL_ENABLED
import ssl 


# @app.before_request
# def redirect_to_https():
#     if request.scheme == 'http':
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)


if __name__ == '__main__':
    if SSL_ENABLED :
        https_server = WSGIServer(('0.0.0.0', SERVER_PORT), app,certfile =SSL_CA_FILE,keyfile =SSL_CA_KEY_FILE)
        https_server.start()
        https_server.serve_forever()
    else:
        http_server = WSGIServer(('0.0.0.0', SERVER_PORT), app)
        http_server.start()
        http_server.serve_forever()
        
    # 如果希望http和https都同时存在，用户访问http自动跳转到https，使用以下配置
        # https_server = WSGIServer(('0.0.0.0', SERVER_PORT), app,certfile =SSL_CA_FILE,keyfile =SSL_CA_KEY_FILE)
        # https_server.start()
        # https_server.serve_forever()
        # http_server = WSGIServer(('0.0.0.0', 80), app)
        # http_server.start()
        # http_server.serve_forever()
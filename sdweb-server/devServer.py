from flask_cors import CORS
from config.setting import SERVER_PORT
import ssl
# from api.user import app
from api.stablediffusion import app
from config.setting import SSL_CA_FILE,SSL_CA_KEY_FILE,SERVER_PORT,SSL_ENABLED

# # 项目根路径
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_PATH)
# sys.path.insert(0, BASE_PATH)  # 将项目根路径临时加入环境变量，程序退出后失效
CORS(app, supports_credentials=True)

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('ai8.live/fullchain.pem', 'ai8.live/privkey.pem')


if __name__ == '__main__':
    # host为主机ip地址，port指定访问端口号，debug=True设置调试模式打开
    # app.run(host="0.0.0.0", port=SERVER_PORT,ssl_context=context, debug=True)
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)


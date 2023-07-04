# 服务端口配置
# Service port configuration
SERVER_PORT = 80

# 请求链接是否开启SSL证书，SSL证书是与你的域名绑定的，如果走Nginx代理进来建议将SSL_ENABLED 改为False，证书可让Nginx提供，如果本应用直接对外提供服务器，端口可改成443，启动证书
# Request link whether to enable SSL certificate. The SSL certificate is bound to your domain name. If you use Nginx proxy to come in, it is recommended to change SSL_ENABLED to False. The certificate can be provided by Nginx. If the application directly provides the server externally, the port can be changed to 443 , start the certificate
SSL_ENABLED = False

# SSL证书文件位置，ca和key文件建议存放到cafile 文件夹下，可以使用./config/sslfile/ca.cer相对路径
# SSL certificate file location, ca and key files are recommended to be stored in the cafile folder, you can use the relative path of ./config/sslfile/ca.cer
SSL_CA_FILE="config\\sslfile\\ai8.live\\fullchain.pem"

# SSL证书密钥KEY文件位置，例如：./config/sslfile/key.cer
SSL_CA_KEY_FILE="config\\sslfile\\ai8.live\\privkey.pem"

#站点和用户客户端之间数据链路二次传输加密
# MD5加密盐值
#Secondary transmission encryption of the data link between the site and the user client
DATA_SALT = "xj93nsd98#%*"

# AES encryption,Key length 16 bits,16位长度密钥，必须16位，这个是aes256算法
DATA_AES_KEY = "nklewdfn9832bwef"

# AES IV ，don't know, please do not change it
DATA_AES_IV = "wefjh32o789dsbcv"

# 生成图片存储位置
FILE_STORE_PATH = "./../sdtemp/"

# 打开系统警告提示，如果不希望提示请设为空
# Open the system warning prompt, if you do not want the prompt, please set it to empty
WARRING_ALERT_INFO = "由于目前AI处于起步阶段，AI自主思考生成内容可能会出现不适年龄段人观看，请您确认您已满18周岁，并在后续生成过程中不生成违法、色情内容。目前我们正在努力让AI变得合法合规"

# Stable Diffusion地址，一般是http://127.0.0.1:7860，也可以改成公网地址将站点和StableDiffusion隔离，比如站点在海外，StableDiffusion在本地
#如果Stable Diffusion和本站点不在同一内网，可以使用frp，ngrok
#推荐：https://github.com/fatedier/frp 支持linux windows macos等系统

# Stable Diffusion address, generally http://127.0.0.1:7860, can also be changed to a public network address to isolate the site from StableDiffusion, for example, the site is overseas, and StableDiffusion is local
#If Stable Diffusion and this site are not on the same intranet, you can use frp, ngrok
#Recommendation: https://github.com/fatedier/frp supports linux windows macos and other systems
REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS = "http://sd.7u.work:9800"
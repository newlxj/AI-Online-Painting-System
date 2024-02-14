# sdweb-mulit-user-website

 [简体中文](https://github.com/newlxj/sdweb-multi-user-website/blob/main/README.md "简体中文") | [English](https://github.com/newlxj/sdweb-multi-user-website/blob/main/README_EN.md "English")


![github](https://github.com/newlxj/sdweb-multi-user-website/blob/dev/images/img11.png?raw=true "github")

![gitee](https://gitee.com/aliu/sdweb-multi-user-website/raw/main/images/img12.png "gitee")



##  介绍#
Sdweb Mulit User Website是基于[AUTOMATIC1111](https://github.com/AUTOMATIC1111 "AUTOMATIC1111") API二次开发的平台，在这个平台上提供了用户账号注册，多用户在线绘画、评分、共享及模型管理等功能，并提供tag自动推荐，在用户不具备AI技能情况下自动推荐很好的tag

如果喜欢请fork和star，谢谢

DEMO 站点：https://ai8.live

## 交流
下方使用介绍图很重要，如果看不见可以去国内gitee站点
https://gitee.com/aliu/sdweb-multi-user-website

github：https://github.com/newlxj/sdweb-Multi-User-Website

有问题请在QQ群：793072950 <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=HUcEcepjpCOulnypuKkmHTx_zIpdy0jv&jump_from=webapi&authKey=3AO/lRIb4uXRBu56Wh19vryYKHIoblAf+cKDAcxmCtKyFWJqsbZ5PWjG9Y9nAZz8"><img border="0" src="https://pub.idqqimg.com/wpa/images/group.png" alt="StableDiffusion-Ai8" title="StableDiffusion-Ai8"></a>交流


## 软件架构
Python 3.10

Flask 2.2.3


## 跨网络解及安全决方案
本项目支持Stable Diffusion Stable Diffusion webui部署在个人PC上，PC在法国，sdweb-mulit-user-website 在新加坡，只要Stable Diffusion webui
主机与sdweb-mulit-user-website 在不同国家地域网络,例如：
![Network-Architecture-Diagram](https://github.com/newlxj/sdweb-multi-user-website/blob/dev/images/Network-Architecture-Diagram.png?raw=true "Network-Architecture-Diagram")
Stable Diffusion webui部署在个人PC上，PC Server在法兰克福，sdweb-mulit-user-website部署在美国机房，只要Stable Diffusion webui能被中国、新加坡、全球各地访问到，sdweb-mulit-user-website面对使用的客户将只知道他们访问的是美国服务器，这样有效避免了黑客攻击等情况。

对于安全方面，我们对客户端用户请求的内容进行了AES加密，每次用户登录会颁发不同的密钥，使得即使没有SSL链路情况下数据传输也是安全的。

## 配置教程
1.请部署https://github.com/AUTOMATIC1111 可以使用github官方部署方式或使用qiuye一键部署

1.sdweb 是项目web工程 ，sdweb-server是项目Python工程
第一次使用，请修改 sdweb-server/config/setting.py

	如果使用https协议， 请将 SSL_ENABLED = True
	SSL_CA_FILE SSL域名证书文件
	SSL_CA_KEY_FILE域名证书key文件
	WARRING_ALERT_INFO 警告提醒，如果为空不会打开弹出警告提醒
	REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS  特别注意：这个协商你的stable-diffusion-webui 地址例如:http://127.0.0.1:7860 ，建议修改这个端口并加上IP白名单策略，不要让其他人访问到127.0.0.1:7860而带来安全隐患。

2.stable-diffusion-webui开启API， 在启动参数加上 `--api` （必须加上）
或者webui-user.bat 中设置为 set COMMANDLINE_ARGS="`--api`"
例如：
```shell
python webui.py   --opt-sdp-attention --no-gradio-queue --device-id=0 --no-half-vae   --disable-safe-unpickle --disable-nan-check --api
```
如果使用的是秋叶启动器，请在高级选项选中 "启用API"
![秋叶设置](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/qiuye-setting.png?raw=true "秋叶设置")

## 安装教程

### 自动安装（Windows)
	InstallAll.bat

### 手动安装（Windows)
	cd sdweb
	npm install
	cd sdweb-server
	python -m venv ai8-env
	ai8-env\Scripts\activate.bat
	pip install -r requirements.txt

### 手动安装（Linux）
	cd sdweb
	npm install
	cd ../
	cd sdweb-server
	python -m venv ai8-env
	ai8-env\Scripts\activate
	pip install -r requirements.txt

### 构建web项目
	buildSdweb.bat
### 启动服务
#### 启动开发环境
	startDevServer.bat
访问地址：http://127.0.0.1
#### 启动生产环境（一般正式环境运行稳定）
	startPordServer.bat
访问地址：http://127.0.0.1 (端口80) 可以配置80和443端口双开

## 使用教程
1.登录
 
默认管理员账号：ai8@gmail.com  密码：1234QWER   如果需要修改请用sqllite工具打开sdweb-server的sdai.db 数据库文件，修改user中的账号密码

数据库打开工具推荐使用：SQLite Expert （https://www.sqliteexpert.com/download.html）

![登录](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/login.png?raw=true)
2.进入创作模式
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img1.png?raw=true)
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img2.png?raw=true)
3.选择模型
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img4.png?raw=true)
设置模型
开启超级模式后，使用快捷键`alt+p` 快捷键会自动弹出stable diffusion 模型选择清单，你可以放缩略图，建议宽高 w512*h256
图片存放是相对路径，例如：modelLogo/counterfeitV2525d.png
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img8.png?raw=true)
4.设置高级参数
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img3.png?raw=true)

5.使用随机tag
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img6.png?raw=true)

6.生成图片
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img7.png?raw=true)
7.查看图片
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img5.png?raw=true)
8.共享图片
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img10.png?raw=true)

### 如果你喜欢，请给我一个star用来鼓励我带来更多开源作品

### 未来计划增加功能

| 序号  |  计划内容 |
| ------------ | ------------ |
| 1  | 用户管理维护  |
| 2  | 接入ChatGPT  |
| 3 | 接入语音识别通过说话生成  |
| 4  | 语音版移动端生成  |
| 5  | 图生图一键自动换衣服、换发型 |
| 6  | 集群模式分布式生成  |
| 7  | 对色情图像进行准确过滤  |


#### 参与贡献

欢迎您一起来构建，创建更强大个性化的stable diffusion




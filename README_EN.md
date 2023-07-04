# sdweb-mulit-user-website
|
 [简体中文](https://github.com/newlxj/sdweb-multi-user-website/blob/main/README.md "简体中文") | [English](https://github.com/newlxj/sdweb-multi-user-website/blob/main/README_EN.md "English")



![github](https://github.com/newlxj/sdweb-multi-user-website/blob/dev/images/img11.png?raw=true "github")

![gitee](https://gitee.com/aliu/sdweb-multi-user-website/raw/main/images/img11.png "gitee")


## introduce
Sdweb Mulit User Website is a platform based on the secondary development of [AUTOMATIC1111](https://github.com/AUTOMATIC1111 "AUTOMATIC1111") API. On this platform, it provides user account registration, multi-user online drawing, scoring, sharing and models Management and other functions, and provide tag automatic recommendation, automatically recommend good tags when users do not have AI skills

If you like it, please fork and star, thank you

DEMO site: https://ai8.live

## comminicate
It is very important to use the introduction picture below, if you can’t see it, you can go to the domestic gitee site
https://gitee.com/aliu/sdweb-multi-user-website

github: https://github.com/newlxj/sdweb-Multi-User-Website
StableDiffusion-Ai8If you have any questions, please communicate 
in the QQ group: 793072950


## Software Architecture
Python 3.10

Flask 2.2.3


## Cross-network solutions and security solutions
This project supports Stable Diffusion Stable Diffusion webui deployed on personal PC, PC in France, sdweb-mulit-user-website in Singapore, as long as Stable Diffusion webui
The host and sdweb-mulit-user-website are in different countries and regions, for example:
![Network-Architecture-Diagram](https://github.com/newlxj/sdweb-multi-user-website/blob/d736f37253ddc656e1285798beb2b431794dc603/images/Network-Architecture-Diagram.png?raw=true "Network-Architecture-Diagram ")
Stable Diffusion webui is deployed on a personal PC, PC Server is in Frankfurt, and sdweb-mulit-user-website is deployed in a computer room in the United States. As long as Stable Diffusion webui can be accessed by China, Singapore, and all over the world, sdweb-mulit-user-website will face Customers who use it will only know that they are visiting a US server, which effectively avoids hacking and other situations.

In terms of security, we perform AES encryption on the content requested by the client user, and issue a different key each time the user logs in, making data transmission safe even without an SSL link.

## Configuration Tutorial
1.sdweb is the project web project, sdweb-server is the project Python project
For the first use, please modify sdweb-server/config/setting.py

	If using https protocol, please set SSL_ENABLED=True
	SSL_CA_FILE SSL domain name certificate file
	SSL_CA_KEY_FILE domain name certificate key file
	WARRING_ALERT_INFO warning reminder, if it is empty, no pop-up warning reminder will be opened
	REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS Special attention: this negotiates your stable-diffusion-webui address, for example: http://127.0.0.1:7860, it is recommended to modify this port and add an IP whitelist policy, do not let others access 127.0.0.1:7860 and pose a safety hazard.

2.stable-diffusion-webui opens the API, add `--api` to the startup parameters (must be added)
Or set COMMANDLINE_ARGS="`--api`" in webui-user.bat
For example:
```shell
python webui.py --opt-sdp-attention --no-gradio-queue --device-id=0 --no-half-vae --disable-safe-unpickle --disable-nan-check --api
```
If you are using the Autumn Leaf Launcher, please check "Enable API" in the advanced options
![Autumn Leaf Setting](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/qiuye-setting.png?raw=true "Autumn Leaf Setting")

## Installation Tutorial

### Automatic installation (Windows)
	InstallAll.bat

### Manual installation (Windows)
	cd sdweb
	npm install
	cd sdweb-server
	python -m venv ai8-env
	ai8-env\Scripts\activate.bat
	pip install -r requirements.txt

### Manual installation (Linux)
	cd sdweb
	npm install
	cd ../
	cd sdweb-server
	python -m venv ai8-env
	ai8-env\Scripts\activate
	pip install -r requirements.txt

### Build the web project
	buildSdweb.bat
### Start the service
#### Start the development environment
	startDevServer.bat
Access address: http://127.0.0.1
#### Start the production environment (generally the formal environment runs stably)
	startPordServer.bat
Access address: http://127.0.0.1 (port 80) can be configured to open both ports 80 and 443

## Tutorial
1. Login
 
Default administrator account: ai8@gmail.com Password: 1234QWER If you need to modify it, please use the sqllite tool to open the sdai.db database file of sdweb-server, and modify the account password in user

Recommended database opening tool: SQLite Expert (https://www.sqliteexpert.com/download.html)

![Login](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/login.png?raw=true)
2. Enter creative mode
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img1.png?raw=true)
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img2.png?raw=true)
3. Select the model
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img4.png?raw=true)
set model
After turning on the super mode, use the shortcut key `alt+p` and the shortcut key will automatically pop up the stable diffusion model selection list, you can put a thumbnail, the recommended width and height are w512*h256
Image storage is a relative path, for example: modelLogo/counterfeitV2525d.png
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img8.png?raw=true)
4. Set advanced parameters
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img3.png?raw=true)

5. Use random tags
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img6.png?raw=true)

6. Generate pictures
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img7.png?raw=true)
7. View pictures
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img5.png?raw=true)
8. Share pictures
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img10.png?raw=true)

### If you like it, please give me a star to encourage me to bring more open source works

### Future plans to add features

| Serial number | Plan content |
| ------------ | ------------ |
| 1 | User Management and Maintenance |
| 2 | Access ChatGPT |
| 3 | Access Speech Recognition Generated by Speak |
| 4 | Voice version mobile terminal generation |
| 5 | Automatically change clothes and hairstyles with one click of the picture |
| 6 | Cluster Mode Distributed Generation |
| 7 | Accurate filtering of pornographic images |


#### Contribute

You are welcome to build together to create a more powerful and personalized stable diffusion

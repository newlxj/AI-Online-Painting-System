# sdweb-mulit-user-website 

## Introduction 
Sdweb Mulit User Website is a secondary development platform based on [AUTOMATIC1111](https://github.com/AUTOMATIC1111 "AUTOMATIC1111") API, which provides user account registration , multi-user online painting, scoring, sharing and model management functions, and provide tag automatic recommendation, automatically recommend a good tag example site if the user does not have AI skills 

: https://ai8.live 

## Software Architecture 
Python 3.10 
Flask 2.2.3 


## Cross-network solution and security solution 
This project supports Stable Diffusion Stable Diffusion webui is deployed on a personal PC, the PC is in France, and sdweb-mulit-user-website is in Singapore, as long as the Stable Diffusion webui 
host and sdweb- mulit-user-website is networked in different countries, for example: 
![Network-Architecture-Diagram](https://github.com/newlxj/sdweb-multi-user-website/blob/d736f37253ddc656e1285798beb2b431794dc603/images/Network-Architecture- Diagram.png?raw=true "Network-Architecture-Diagram") 
mulit-user-website is deployed in different countries and regions, for example: Stable Diffusion webui is deployed on a personal PC, the PC is in the United States, sdweb-mulit-user-website is in Singapore, as long as the Stable Diffusion webui can be accessed by the Singapore server, sdweb- -user-website customers will only know that they are visiting the Singapore server, which effectively avoids hacking and other situations. 

For security and convenience, we encrypt the content requested by the client user with AES, and issue a different key each time the user logs in, making data transmission safe even without an SSL link. 

## Configuration Tutorial
1. sdweb is the project web project, sdweb-server is the project Python project 
For the first time use, please modify sdweb-server/config/setting.py 

	If you use the https protocol, please set SSL_ENABLED = True 
	SSL_CA_FILE SSL domain name certificate file 
	SSL_CA_KEY_FILE domain name certificate key File 
	WARRING_ALERT_INFO Warning reminder, if it is empty, it will not open a pop-up warning reminder 
	REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS Special attention: this negotiates your stable-diffusion-webui address For example: http://127.0.0.1:7860, it is recommended to modify this port and add an IP whitelist Policy, do not allow other people to access 127.0.0.1:7860 and bring security risks.  
``` 
If you are using the qiuye Launcher, please select "Enable API" in the advanced options

2.stable-diffusion-webui opens the API, add `--api` to the startup parameters (must be added)
Or set COMMANDLINE_ARGS="`--api`" in webui-user.bat 
For example: 
```shell 
python webui.py --opt-sdp-attention --no-gradio-queue --device-id=0 --no-half-vae --disable-safe-unpickle --disable-nan-check --api 
![qiuye Settings](https://github.com/newlxj/sdweb-multi-user-website/blob /main/images/qiuye-setting.png?raw=true "Autumn Leaves Setting") 

## Installation tutorial 

### Automatic installation (Windows) 
	InstallAll.bat 

### Manual installation (Windows) 
	cd sdweb 
	npm install 
	cd sdweb- server 
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

### Build web project 
	buildSdweb.bat 
### Start service 
#### Start development environment  
	startDevServer.bat 
Access address: http://127.0.0.1:9999
#### Start production environment ( Generally, the official environment runs stably) 
	startPordServer.bat 
access address: http://127.0.0.1 (port 80) can be configured to double open ports 80 and 443 

## Tutorial 
1. Login 
! [Login](https://github.com/ newlxj/sdweb-multi-user-website/blob/main/images/login.png?raw=true) 
2. Enter creative mode 
![](https://github.com/newlxj/sdweb-multi-user-website /blob/main/images/img1.png?raw=true) 
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img2.png?raw=true ) 
3. Select model 
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img4.png?raw=true) After 
setting the model 
to open the super mode, use the shortcut key `alt+p` to automatically pop up the stable diffusion model selection list, you can put a thumbnail, and the recommended width and height are w512* h256 
image storage is a relative path, for example: modelLogo/counterfeitV2525d.png 
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img8.png?raw=true) 
4. Set advanced parameters
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img3.png?raw=true) 

5. Use random tag 
![](https://github .com/newlxj/sdweb-multi-user-website/blob/main/images/img6.png?raw=true) 

6. Generate images 
![](https://github.com/newlxj/sdweb-multi-user -website/blob/main/images/img7.png?raw=true) 
7. View pictures 
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img5 .png?raw=true) 
8. Share pictures 
![](https://github.com/newlxj/sdweb-multi-user-website/blob/main/images/img10.png?raw=true) 

### If you like it, please give me a star to encourage me to bring more open source works 

#### Participate in contributions 

1. Fork this warehouse 
2. Create a new Feat_xxx branch 
3. Submit code 
4. Create a new Pull Request


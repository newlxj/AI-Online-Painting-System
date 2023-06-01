from http.client import HTTPException
import io
import os
from flask import render_template, send_file,g
from flask import Flask, jsonify, request, Response, session,abort,redirect
from werkzeug.exceptions import Unauthorized
from api.CryptoEncrypt import CryptoEncrypt
from api.SaveData import DataToDB
import requests
import json
import copy
import base64
import hashlib
import datetime
from PIL import Image
from config.setting import FILE_STORE_PATH ,REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS,WARRING_ALERT_INFO
from api.webuiapi import  WebUIApi
from io import BytesIO
import datetime

# 检查服务器在线过期事件
CHECK_SERVER_ONLINE_EXPIR_TIME = 0
# 检查服务器是否在线 1在线 0不在线
CHECK_SERVER_IS_ONLINE = "1"
# 服务器离线时间
SERVER_OFFLINE_TIME =0
# 平台总图片数
ALL_IMAGES_COUNT = ""
 
    
# app = Flask(__name__)
app = Flask(__name__, template_folder="../templates",
            static_folder="../static", static_url_path="/")
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示
# 
wApi = WebUIApi(baseurl= REMOTE_STABLE_DIFFUSION_SERVER_ADDRESS+"/sdapi/v1")
# g.cryptoFunc = CryptoEncrypt()
# 首页
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/createModel')
def createModel():
    return app.send_static_file('index.html')

@app.route('/viewer')
def viewer():
    return app.send_static_file('index.html')


# 创建模型
@app.errorhandler(400)
def handle_bad_request(e):
    return '错误请求', 400   #返回错误信息

@app.route("/api/create", methods=['POST'])
def create():
    jsonData  = decryptData(None)
    print(jsonData)
    if jsonData["imageBatchCount"] > 10:
        return ""

    if jsonData["imageBatchSize"] > 4:
        return ""

    if jsonData["step"] > 60:
        return ""
    
    if jsonData["cfgScale"]== None or jsonData["cfgScale"] >20:
        jsonData["cfgScale"]= 7.5

    if jsonData["sizeh"] > 2000 or jsonData["sizew"] > 2000:
        return ""
    
    if jsonData["samplerIndex"] == None or jsonData["samplerIndex"] == "":
       jsonData["samplerIndex"] = 'Euler a'
    
    prompt = jsonData["prompt"]
    prompt = prompt.replace("nsfw", "sfw")

    negative_prompt = jsonData["negative_prompt"]
    negative_prompt = negative_prompt.replace("sfw", "nsfw")
    print(jsonData["upscaleB"])
    jsonobj = wApi.txt2img(enable_hr=jsonData["upscaleB"],denoising_strength = 0.7,prompt=prompt,negative_prompt=negative_prompt,seed=jsonData["seed"],subseed=jsonData["seed"],batch_size=jsonData["imageBatchCount"],n_iter= jsonData["imageBatchSize"],steps=jsonData["step"],cfg_scale= jsonData["cfgScale"],width=jsonData["sizew"],height=jsonData["sizeh"],sampler_index=jsonData["samplerIndex"])
    info = jsonobj.info 
    all_seeds = info["all_seeds"]
    strImage = jsonobj.images
    imgsLen = len(strImage)
    seedsLen = len(all_seeds)
    imgpathArr = []
    hires_upscale = 1
    hires_upscaler = ""
    eta = ""

    if len(info["extra_generation_params"]) > 1:
        hires_upscale = info["extra_generation_params"]["Hires upscale"]
        hires_upscaler = info["extra_generation_params"]["Hires upscaler"]
        eta = info["extra_generation_params"]["Eta"]

    imagesInfo = {
        "prompt": info["prompt"],
        "negative_prompt": info["negative_prompt"],
        "step": info["steps"],
        "cfg_scale": info["cfg_scale"],
        "sizew": info["width"],
        "sizeh": info["height"],
        "model_hash": info["sd_model_hash"],
        "seed": info["seed"],
        "denoising_strength": 1, 
        "hires_upscale": hires_upscale,
        "hires_upscaler": hires_upscaler,
        "Eta": eta
    }
    print(imagesInfo)
    imageInfoStr = json.dumps(imagesInfo)
    imageInfoStr = imageInfoStr.replace(',', '')
    imageInfoStr = imageInfoStr.replace(' ', '')
    md5 = hashlib.md5(imageInfoStr.encode()).hexdigest()
    
    
    imagesInfo["seed"] = info["seed"]
    date_str = datetime.date.today().strftime('%Y%m%d')
    for i in range(imgsLen):
        img = strImage[i]
        # 处理gird情况，grid不存储
        if seedsLen != imgsLen and i == 0:
            seed = -200
            continue
        else:
            seed = all_seeds[i-1]
            img_data = base64.b64decode(strImage[i])
            if not os.path.exists(FILE_STORE_PATH+date_str):
                os.makedirs(FILE_STORE_PATH+date_str)
            imageDir = date_str + "/" + \
                str(imagesInfo["seed"]) + "_" + str(seed) + "_image.png"
            filePath = FILE_STORE_PATH + imageDir
            obj = {"seed": str(seed), "path": imageDir}
            imgpathArr.append(obj)

            with open(filePath, "wb") as f:
                f.write(img_data)
                f.close()
            imagesInfo["image_md5_id"] = md5
    imagesInfo["sub_seed_path"] = imgpathArr
    imagesTagMd5Arr = DataToDB.saveImages(imagesInfo,g.userEmail,g.userIp)
    if imagesTagMd5Arr == None:
        return ""
    imagesInfo["sub_seed_path"] = imagesTagMd5Arr
    return encryptData(imagesInfo,True) 

# 检查生成进度


@app.route("/api/process", methods=['POST'])
def process():
    response =wApi.get_progress()
    return encryptData(response,True)

@app.route("/api/interrupt", methods=['POST'])
def interrupt():
    response =wApi.post_interrupt()
    return ""

@app.route("/api/deleteImage", methods=['POST'])
def deleteImage():
    jsonData  = decryptData(None)
    # 检查当前用户是否是本人，如果是管理员也允许删除
    id = jsonData["id"]
    if id == None or id == '':
        return encryptData({"code":400,"flag":False},True)
    
    list = DataToDB.getImageSeedInfo(id)
    if len(list) == 0:
        return encryptData({"code":200,"flag":False},True)
    
    if DataToDB.checkUserIsAdmin(g.userEmail) == True or list[0]["user_id"] == g.userEmail:
        DataToDB.deleteImages(jsonData["id"])
        return encryptData({"code":200,"flag":True},True)
    print("没有权限删除....")
    return encryptData({"code":200,"flag":False},True) 


@app.route("/api/share", methods=['POST'])
def shareImage():
    jsonData  = decryptData(None)
    id = jsonData["id"]
    shareflag = jsonData["flag"]
    if id == None or id == '' or shareflag == None or shareflag == '':
        return encryptData({"code":400,"flag":False},True)
    
    list = DataToDB.getImageSeedInfo(id)
    if len(list) == 0:
        return encryptData({"code":200,"flag":False},True)
    
    if DataToDB.checkUserIsAdmin(g.userEmail) == True or list[0]["user_id"] == g.userEmail:
        DataToDB.updateImageSeedShareStatus(id,shareflag)
        return encryptData({"code":200,"flag":True},True)
    
    # 图片是不是本人的 ，当前是否管理员操作
    print("这个图片属于"+ list[0]["user_id"]+" ，你没权限共享操作，你是："+ g.userEmail)
    return encryptData({"code":200,"flag":False},True) 
    
@app.route("/readTags")
def readTags():
    jsonx = [{ 
        "title": "红发少女，在樱花下",
        "seed": "1033881260",
        "step": 20,
        "hires_upscale": 1,
        "sizew": 512,
        "sizeh": 512,
        "prompt": "eromanga,(loli:1.5),(extremely detailed CG unity 8k wallpaper,masterpiece, best quality, ultra-detailed), (best illumination, best shadow, an extremely delicate and beautiful), dynamic angle, floating, finely detail, Depth of field (bloom), (shine), glinting stars,(watercolor_medium), (painting), (sketch),white and pink wet hanfu| pajamas, pink thighhighs,keep hands on the back, smile, look at viewer, sakura and Jasmine background, long_flowing_hair, Jasmine Petals white hair, hair between wet breasts, sakura hair bow, highly detailed, high resolution, cinematic lighting, highly detailed eyes, (solo), game_cg,1girl, Princess, bangs, blue sakura, detailed_foreground, blush, medium breasts, cherry_blossoms, eyebrows_visible_through_hair, falling_petals, floating_hair, sakura, hair_flower, hair_ornament, leaves_in_wind, long_hair, long_sleeves, looking_at_viewer, sakura petals,sakura petals_on_liquid, pink sakura flower, pink_hair, rose_petals, see-through, solo, spring_(season), upper_body, very_long_hair, wind, blue and red eyes,torino",
        "negative_prompt": "(((simple background))),ugly,lowres, bad anatomy,worst quality, low quality, normal quality, [:((No more than one thumb, index finger, middle finger, ring finger and little finger on one hand),(mutated hands and fingers:1.5 ), fused ears, one hand with more than 5 fingers, one hand with less than 5 fingers,):0.5],bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, Missing limbs, three arms, bad feet, text font ui,signature, blurry, malformed hands, long neck, mutated hands and fingers :1.5). (long body :1.3),(mutation ,poorly drawn :1.2), disfigured, malformed, mutated, multiple breasts, futa, yaoi, three legs, huge breasts"
    }]

# 下载本地文件
@app.route("/api/readImage")
def readImage():
    id = request.args.get('id')
    # 空 或0 缩小到40%  1 缩放到 60% 2 缩放到 80%  3 缩放到 100%
    type = request.args.get('t')
    list = DataToDB.getImageSeedInfo(id)
    if len(list) == 0:
        return ""
    image_path = str(list[0]["image_path"])
    print(FILE_STORE_PATH + image_path)
    # 从磁盘读取原始图片
    original_image = Image.open(FILE_STORE_PATH + image_path)

    # 缩放图片
    width, height = original_image.size
    bw = 0.0
    bh = 0.0

    if type == None or type == "1":
        bw = 0.4
        bh = 0.4
    elif type == "2":
        bw = 0.6
        bh = 0.6
    elif type == "3":
        bw = 0.8
        bh = 0.8
    elif type == "4":
        bw = 1.0
        bh = 1.0

    if type != "4":
        new_size = (int(width * bw), int(height * bh))
        resized_image = original_image.resize(new_size)
        # 将缩放后的图片保存到内存中
        buffer = io.BytesIO()
        resized_image.save(buffer, format='png')
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png')
    # 从内存中读取缩放后的图片并返回给请求者
    print(os.getcwd()+FILE_STORE_PATH + image_path)
    return send_file(os.getcwd()+FILE_STORE_PATH + image_path, mimetype='image/png', as_attachment=True)


@app.route('/api/photos', methods=['POST'])
def getPhotos():
    jsonData  = decryptData(None)
    nextSize = jsonData["size"] #request.args.get('size')
    print(nextSize)
    imageJson = DataToDB.getImagesList(nextSize, 10, g.userEmail,g.userRole)
    print(imageJson)
    return encryptData(imageJson,True)  #jsonify(imageJson)

 
@app.route('/api/star', methods=['POST'])
def star():
    jsonData  = decryptData(None)
    # postData = request.get_json()  # 根据 Content-Type 解码请求的 body
    # imageId = postData.get('id')
    starNum = DataToDB.saveStar(jsonData["id"],   g.userEmail, g.userIp)
    return encryptData( {"starNum": starNum},True)

@app.route('/api/listModel', methods=['POST'])
def listSdModel():
    response =wApi.get_sd_models()
    print(response)
    listJson = response

    modelSetting = []
    with open('config/config.json', 'r') as f:
        modelSetting = json.load(f)  # 读取文件内容
    f.close()
    for model in listJson:
        del model["filename"]
        del model["hash"]
        del model["model_name"]
        del model["sha256"]
        del model["config"]
        for mset in modelSetting:
            if model["title"] == mset["title"]:
                model["showName"] = mset["showName"]
                model["miniLogo"] = mset["miniLogo"]
                model["desc"] = mset["desc"]
                model["selectedx"] = mset["selectedx"]
                if "order" in mset :
                    # print(mset["order"])
                    model["order"] = mset["order"]
                else:
                    model["order"] =""
                break
            else:
                model["showName"] = ""
                model["miniLogo"] = ""
                model["desc"] = ""
                model["selectedx"] = False
                model["order"] = ""
    return encryptData(listJson,True) 
    # return jsonify(listJson)


@app.route('/api/changeModel', methods=['POST'])
def changeModel():
    jsonData  = decryptData(None)
    modelId = jsonData["modelId"]
    wApi.set_options({"sd_model_checkpoint":modelId})
    return ""
    

@app.route('/api/saveSdModel', methods=['POST'])
def saveSdModel():
    # postData = request.data.decode('utf-8')  # 根据 Content-Type 解码请求的 body
    # str = jsonify(postData)
    # print(str)
    jsonData  = decryptData(None)
    str = json.dumps(jsonData)
    print(jsonData)
    with open('config/config.json', 'w') as file:
        file.write(str)
    file.close()
    return encryptData({"code": "200", "msg": ""},True) 


@app.route('/api/getModelImg')
def getModelImg():
    mid = request.args.get('mid')
    with open('config/config.json', 'r') as f:
        modelSetting = json.load(f)  # 读取文件内容
    f.close()
    for model in modelSetting:
        if model["number"] == mid:
            if model["miniLogo"] != "":
                current_path = os.getcwd()
                return send_file(current_path+"/"+model["miniLogo"], mimetype='image/png')
        # print(model["title"])
    return ""

SAMPLER_LIST = []

@app.route('/api/getSampler', methods=['POST'])
def getSampler():
    if len(SAMPLER_LIST) == 0 :
        samplerArr = wApi.get_samplers()
        for sampler in samplerArr:
            SAMPLER_LIST.append(sampler["name"])
    return encryptData(SAMPLER_LIST,True)


@app.route('/api/getCheckModelList', methods=['POST'])
def getModelList():
    str = ""
    with open('config/config.json', 'r') as f:
        str = f.read()  # 读取文件内容
    f.close()
    return encryptData(str,False)  

@app.route('/api/test')
def test():
    # WebUIApi.txt2img()
    wApi = WebUIApi()
    my_list = wApi.txt2img(steps=20,negative_prompt="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",prompt=" (masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper),kawaii, Round white eyebrows,night, night, artbook, highres, little girl, ((chibi)), (hair over shoulder), white hair, (ahoge), (embarrassed ), (blush), (cat_ears), (wide eyed), (slit pupils ), ((fangs)), (red eyes), (medium breasts), (japanese_clothes), halo, (looking up),")
   
    print(my_list) 
    for imgdt in my_list.images:
        data = base64.b64decode(imgdt)
        # 将二进制数据写入磁盘
        with open("f://example_copy.png", "wb") as f:
            f.write(data)
        f.close()
    return ""


@app.route('/api/getAitagData')
def getAitagData(): 
    url = 'https://api.aitag.top/tagv2'
    data = {"method": "get_tags_from_sub", "sub": "魔导师分享", "page": 1}
    response = requests.post(url, json=data)
    json_data = json.loads(response.text)
    resultData = json_data["result"]
    DataToDB.setAitagData(resultData)
    return "https://api.aitag.top/ 成功写入到 tags表，请勿重复执行会插入重复数据"


@app.route('/api/getTag', methods=['POST'])
def getTag(): 
    tagObj = DataToDB.getTag()
    return encryptData(tagObj,True)
    
@app.route('/api/login', methods=['POST'])
def login():
    postData = request.data.decode('utf-8')  # 根据 Content-Type 解码请求的 body
    print(postData)
    data = json.loads(postData)
    email = data['email']
    password = data['password']
    userInfo = DataToDB.login(email,password,g.userIp,g.userAgent)
    print(userInfo)
    if userInfo["status"] == '1':
        print(g.userIp)
        g.userRole = userInfo["role"]
        token = createToken(email,g.userRole,g.userIp)
        return jsonify({'code': 0, 'msg': '登录成功','token':token})
    else:
        return jsonify({'code': -1, 'msg': '登录失败'})
    
@app.route('/testx')
def testx():
    jsonData  = g.cryptoFunc.decrypt("r78JzPkLwrSeKml+UjHIAvkdtoaJ2+AFeb3r56ztGmEs+bplJ4aaBToVYG6Gopry")
    return jsonify(jsonData)
    

    
# 处理注册请求
@app.route('/api/reg', methods=['POST'])
def register():
    print(g.userIp)
    data = request.json
    email = data['email']
    password = data['password']
    if email==None or email == "" or len(email) ==0 :
        return ""
    if password==None or email == "" or  len(email) ==0 :
        return ""
    
    regStatus = DataToDB.register(email,password,g.userIp,g.userAgent)
    if regStatus == 1:
        token = createToken(email,'user',g.userIp)
        return jsonify({'code': 1, 'msg': '注册成功','token':token})
    elif regStatus == 2:
        return jsonify({'code': 2, 'msg': '邮箱已注册'})
    else:
        return jsonify({'code': -1, 'msg': '注册失败'})

def createToken(email,role, user_ip):
    # 获取当前时间戳
    current_timestamp = int(datetime.datetime.now().timestamp())
    expire_timestamp = int((datetime.datetime.now() + datetime.timedelta(minutes=60*24*1)).timestamp())
    print(email + ","+user_ip+","+ role + ","+str(current_timestamp)+","+str(expire_timestamp))
    token = g.cryptoFunc.encrypt(email + ","+user_ip+","+ role + ","+str(current_timestamp)+","+str(expire_timestamp))
    return token

def checkToken(token,ip):
    current_timestamp = int(datetime.datetime.now().timestamp())
    # 解密token
    arr = token.split(",")
    # 时间是否过期
    if int(arr[4]) <=current_timestamp:
        return None
    # IP是否变化
    if arr[1]!= ip:
        return None
    # 设置用户信息
    g.userEmail = arr[0]
    g.userLoginIp = arr[1]
    g.userRole = arr[2]
    g.userexpire = arr[4]
    return arr

@app.before_request
def process_request():
    if '/api/' not in request.path: 
        return
    # method = request.method
    g.userIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    g.userAgent = request.headers.get('User-Agent')
    g.cryptoFunc = CryptoEncrypt()
    print(request.path)
    if '/api/login' not in request.path and  '/api/reg' not in request.path :
        token = request.cookies.get("token")
        print(token)
        # auth = request.headers.get('Authorization')
        if token != '' and token != None:
            try:
                tokenUserInfo = g.cryptoFunc.decrypt(token)
                tokenArr = checkToken(tokenUserInfo,g.userIp)
                if tokenArr == None:
                    raise Unauthorized()
                md5key = hashlib.md5(token.encode()).hexdigest()[8:24]
                # print(md5key)
                g.cryptoFunc.setCryptoKey(md5key)
            except Exception as e:
                raise Unauthorized()
        else:
            raise Unauthorized()
@app.route('/api/checkx', methods=['POST'])
def checkx():
    global CHECK_SERVER_ONLINE_EXPIR_TIME
    global CHECK_SERVER_IS_ONLINE
    # 平台总图片数
    global ALL_IMAGES_COUNT 
    global SERVER_OFFLINE_TIME
    # 提示警告
    
    # print(robottxt.ok)
    
    if CHECK_SERVER_ONLINE_EXPIR_TIME < int(datetime.datetime.now().timestamp()) :
        CHECK_SERVER_ONLINE_EXPIR_TIME = int(datetime.datetime.now().timestamp()+40) # 40秒后才能再次检查
        try:
            robottxt = wApi.get_prompt_styles()
            if robottxt.ok:
                CHECK_SERVER_IS_ONLINE = "1"
                SERVER_OFFLINE_TIME = 0
            else:
                if CHECK_SERVER_IS_ONLINE == "1": # 如果之前就是1表示之前是在线现在离线了
                    SERVER_OFFLINE_TIME = int(datetime.datetime.now().timestamp())
                CHECK_SERVER_IS_ONLINE = "0"
        except Exception as e:
            if CHECK_SERVER_IS_ONLINE == "1": # 如果之前就是1表示之前是在线现在离线了
                SERVER_OFFLINE_TIME = int(datetime.datetime.now().timestamp())
            CHECK_SERVER_IS_ONLINE = "0"
            # print('请求异常:', e)
        ALL_IMAGES_COUNT = str(DataToDB.getSystemAllImage() ) 
    offline_m=0
    if SERVER_OFFLINE_TIME !=0 :
        offline_m = (int(datetime.datetime.now().timestamp()) - SERVER_OFFLINE_TIME) /60
    jsonObj= {"ol":CHECK_SERVER_IS_ONLINE,"offline":int(offline_m) ,"imgCount":ALL_IMAGES_COUNT ,"warring":WARRING_ALERT_INFO}
    return encryptData(jsonObj,True)
 
  
def decryptData(ddata):
    if ddata == None or ddata == '':
       ddata = request.data.decode('utf-8') 
    return json.loads(g.cryptoFunc.decrypt(ddata)) 

def encryptData(edata,jsonToString):
    if jsonToString:
        edata = json.dumps(edata)
    endata = g.cryptoFunc.encrypt(edata)
    return endata
        
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    # 如果抛出了 Unauthorized 异常，则返回 401 状态码和错误信息
    return "Unauthorized: {}".format(e), 401
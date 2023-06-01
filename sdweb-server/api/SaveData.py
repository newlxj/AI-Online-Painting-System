import hashlib
import json
from flask import jsonify
from sqlalchemy import Column, Integer, Sequence, create_engine
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from json import dumps
from config.setting import FILE_STORE_PATH
import time
import os


db_connect = create_engine("sqlite:///sdai.db", pool_size=5,
                           max_overflow=10, pool_recycle=3600)
conn = db_connect.connect()


class DataToDB:
    def saveImages(imagesJson, userId, userIp):
        imagesTagMd5Arr = []
        try:
            print(imagesJson)
            try:
                result = conn.execute(text(
                    "insert into images ('image_md5_id','prompt','negative_prompt','step','cfg_scale','seed','sizew','sizeh','model_hash','denoising_strength','hires_upscale','hires_upscaler','Eta','user_id','create_ip') values(:image_md5_id, :prompt,:negative_prompt,:step,:cfg_scale,:seed,:sizew,:sizeh,:model_hash,:denoising_strength,:hires_upscale,:hires_upscaler,:Eta ,:user_id,:create_ip)"), [{"image_md5_id": imagesJson["image_md5_id"], "prompt": imagesJson["prompt"], "negative_prompt": imagesJson["negative_prompt"], "step": imagesJson["step"], "cfg_scale": imagesJson["cfg_scale"], "seed": imagesJson["seed"], "sizew": imagesJson["sizew"], "sizeh": imagesJson["sizeh"], "model_hash": imagesJson["model_hash"], "denoising_strength": imagesJson["denoising_strength"], "hires_upscale": imagesJson["hires_upscale"], "hires_upscaler": imagesJson["hires_upscaler"], "Eta": imagesJson["Eta"],"user_id":userId,"create_ip":userIp}])
            except IntegrityError as e1:
                print(e1._message)
                conn.rollback()
            # 执行插入操作
            # 获取result中的id
            for sub_seed_path in imagesJson["sub_seed_path"]:
                # sharetype -1:删除 0:私密 1:公开
                image_tag_md5_id = hashlib.md5(
                    (imagesJson["image_md5_id"]+str(sub_seed_path["seed"])).encode()).hexdigest()
                conn.execute(text(
                    "insert into ImagesSeed ('image_tag_md5_id','image_md5_id','parent_seed','seed','image_path','user_id','create_ip') values (:image_tag_md5_id,:image_md5_id,:parent_seed,:seed,:image_path,:user_id,:create_ip)"), [{"image_tag_md5_id": image_tag_md5_id, "image_md5_id": imagesJson["image_md5_id"], "parent_seed": str(imagesJson["seed"]), "seed": str(sub_seed_path["seed"]), "image_path":sub_seed_path["path"],"user_id":userId,"create_ip":userIp}])
                imagesTagMd5Arr.append(
                    {"seed": str(sub_seed_path["seed"]), "image_tag_md5_id":  image_tag_md5_id})
                # +image_tag_md5_id
            conn.commit()
        except IntegrityError as e:
            conn.rollback()
            return None
            # 将image_md5_id和seed查询出来
            # if 'UNIQUE' in str(e):
            #     # 处理重复数据异常
            #     return
        # finally:
            # conn.close()
        # print(query)
        return imagesTagMd5Arr

    def getImageSeedInfo(id):
        querySql = conn.execute(
            text("select * from ImagesSeed where image_tag_md5_id =:image_tag_md5_id "), [{"image_tag_md5_id": id}])
        list = [dict(zip(tuple(querySql.keys()), i))
                for i in querySql.cursor]
        return list
 
    def deleteImages(id):
        filename =""
        # 查询图片位置
        
        list = DataToDB.getImageSeedInfo(id)
        if len(list) == 0:
            return
        imagePath = str(list[0]["image_path"])
        if os.path.exists(FILE_STORE_PATH+imagePath):
            os.remove(FILE_STORE_PATH+imagePath)
        conn.execute(text("delete from ImagesSeed where image_tag_md5_id =:image_tag_md5_id "), [{"image_tag_md5_id": id}])
        conn.commit()
    
    def checkUserIsAdmin(email):
        query = conn.execute(
            text("select role from user where email = :email "), [{"email": email}])
        role = query.fetchone()
        if role != None and len(role) > 0:
            grole = role[0]
            if str(grole) == "admin":
                return True
        return False

    def getImagesList(num, size,userId,userRole):
        roleAnd=""
        shareAnd = " or b.share = 1 "
        if userRole != "admin":
            roleAnd = " and (b.user_id = '"+userId+"' " + shareAnd +") "
        
            
        querySqlCount = "select count(*) as count from imagesSeed b where 1=1 " + roleAnd 
        querySqlBase = "select a.image_name,a.prompt,a.negative_prompt,a.step,a.sampler,a.cfg_scale,a.sizew,a.sizeh,a.denoising_strength,a.hires_upscale,a.hires_upscaler,a.Eta,b.image_tag_md5_id,b.seed,b.star,b.create_ip,b.user_id,b.share from images a,imagesSeed b where a.image_md5_id = b.image_md5_id " + roleAnd + " order by  b.createtime desc limit :num,:size "
        queryCount = conn.execute(
            text(querySqlCount))
        countNum = queryCount.fetchone()[0] 
        # print(countNum)
        imagesList = {"totalSize": countNum, "pageNum": num}
        queryBase = conn.execute(
            text(querySqlBase), [{"num": num, "size": size}])
        listImages = [dict(zip(tuple(queryBase.keys()), i))
                      for i in queryBase.cursor]
        for i in listImages:
            if userId == i["user_id"] or roleAnd =="" :
                i["self"] =1
            else:
                i["self"] = 0
            i["create_ip"] = i["create_ip"][0:6]+"..." 
            i["user_id"] = i["user_id"][0:6]+"..." 
        imagesList["rows"] = listImages
        return imagesList
    
    
    def getSystemAllImage():
        querySqlCount = "select count(*) as count from imagesSeed "  
        queryCount = conn.execute(
            text(querySqlCount))
        return queryCount.fetchone()[0] 
        
    def saveStar(image_tag_md5_id, user_id, star_ip):
        try:
            conn.execute(text(
                "insert into images_star ('image_tag_md5_id','user_id','star_ip') values(:image_tag_md5_id,:user_id,:star_ip)"), [{"image_tag_md5_id": image_tag_md5_id, "user_id": user_id, "star_ip": star_ip}])
            conn.execute(text(
                "update imagesSeed set star=star+1 where image_tag_md5_id = :image_tag_md5_id"), [{"image_tag_md5_id": image_tag_md5_id}])
            result = conn.execute(text(
                "select star from  imagesSeed where image_tag_md5_id = :image_tag_md5_id"), [{"image_tag_md5_id": image_tag_md5_id}])
            starNum = result.fetchone()[0]

            conn.commit()
            return starNum
        except IntegrityError as e1:
            conn.rollback()
            # print(e1)
            if 'UNIQUE' in str(e1):
                # 处理重复数据异常
                print(
                    "重复数据异常.................................xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return
    # 查询模型表

    def getModelList():
        querySql = "select model_id ,model_zh_name,model_title,model_image,model_default from model"
        result = conn.execute(text(querySql))
        list = [dict(zip(tuple(result.keys()), i))
                for i in result.cursor]
        return list
    
    def setAitagData(json_data):
        for item in json_data:
            conn.execute(text("insert into tags (name, desc, image) values(:name,:desc,:image)"), [{"name": item['name'], "desc": item['desc'], "image": item['image']}])
            conn.commit()
            
    def getTag():
        querySql = conn.execute(
            text("SELECT name,desc,image_md5_id FROM tags ORDER BY RANDOM() LIMIT 3"))
        list = [dict(zip(tuple(querySql.keys()), i))
                for i in querySql.cursor]
        return list
    def updateImageSeedShareStatus(imageMd5Id,shareflag):
        conn.execute(text(
                "update imagesSeed set share = :share  where image_tag_md5_id = :image_tag_md5_id"), [{"share":shareflag,"image_tag_md5_id": imageMd5Id}])
        
        
    def login(email, password,user_ip,user_agent):
        query = conn.execute(
            text("select status,role from user where email=:email and password =:password "), [{"email": email,"password": password}])
        fetchall = query.fetchone()
        result ={"status":"","role":""}
        if fetchall != None :
            result["status"] = fetchall[0]
            result["role"] = fetchall[1]
            return result
        return None
    
    def register(email,password,user_ip,user_agent):
        try:
            conn.execute(text("insert into user (email, password, login_ip,user_agent) values(:email,:password,:login_ip,:user_agent)"), [{"email": email, "password": password, "login_ip": user_ip, "user_agent": user_agent}])
            conn.commit()
            return 1
        except IntegrityError as e1:
            conn.rollback()
            print(e1)
            if 'UNIQUE' in str(e1):
                print("邮箱已注册")
                return 2
        return -1
    
    
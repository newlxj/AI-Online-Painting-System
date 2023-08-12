<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-row :gutter="16">
        <el-col :span="24" style="padding-left: 3vw;">
            <el-space wrap :size="15" class="assddw">
                <el-card v-for="(image, index) in images" :key="index" class="box-card"
                    :body-style="{ padding: '20px', width: '210px' }">
                    <el-tooltip class="box-item" effect="dark" content="删除" placement="bottom-end">
                        <el-button v-show="image.imageData.self == 1" type="danger" icon="delete" circle
                            @click="deleteImage(index, image.image_tag_md5_id, image.imageData.user_id)" style=""
                            class="deleteButton" />
                    </el-tooltip>

                        <el-popconfirm confirm-button-text="确定" cancel-button-text="不" :icon="InfoFilled"
                            icon-color="#626AEF" title="共享后其他人都能看见你的图片，确定共享的图片不包含色情、政治、暴力内容?" @confirm="shareImageStatus(image.imageData, 1)"
                            @cancel="cancelEvent">
                            <template #reference>
                                <el-button v-show="image.imageData.self == 1 &&  image.imageData.share == 0" type="warning" icon="share" 
                                    style="" class="shareButton" >共享</el-button>
                            </template>
                        </el-popconfirm>

                    <el-tooltip class="box-item" effect="dark" content="图片已共享，所有人都能看见，点击取消共享" placement="bottom-end">
                        <el-button v-show="image.imageData.self == 1 && image.imageData.share == 1" type="warning"
                            icon="CloseBold" circle @click="shareImageStatus(image.imageData, 0)" style=""
                            class="shareButton" />
                    </el-tooltip>

                    <div class="card-content">
                        <el-image name="test" lazy :ref="'image_' + image.image_tag_md5_id" class="album-image shadow"
                            :key="index" style="text-align: center; cursor: pointer;" :src="image.url" :zoom-rate="1.2"
                            :initial-index="4" fit="cover" :error="handleImageError" :hide-on-click-modal="false"
                            :z-index="22" @click="showImageDialog(image.imageData)" />

                        <div style="padding: 14px">

                            <span class="time text-ellipsis">{{ image.strPromptShort
                            }}</span>
                            <div class="time">图片种子：{{ image.seed }}</div>
                            <div style="display:none" :ref="'prompts_' + image.image_tag_md5_id">{{ image.strPrompt }}</div>
                            <div class="bottom">
                                <el-tooltip class="box-item" effect="dark" content="拷贝关键词" placement="bottom-end">
                                    <el-button type="primary" icon="CopyDocument" circle
                                        @click="copyPrompt(image.image_tag_md5_id)" style="margin-left: 20px;" />
                                </el-tooltip>
                                <el-tooltip class="box-item" effect="dark" content="下载图片" placement="bottom-end">
                                    <el-button type="primary" icon="Download" circle
                                        @click="downloadImg(image.image_tag_md5_id)" style="margin-left: 20px;" />
                                </el-tooltip>
                                <el-tooltip class="box-item" effect="dark" content="将该图片描绘词复制到 <br/>'希望出现的内容中'" raw-content
                                    placement="bottom">
                                    <el-button type="primary" icon="MagicStick" circle @click="copyToInput(image.imageData)"
                                        style="margin-left: 20px;" />
                                </el-tooltip>
                                <el-tooltip class="box-item" effect="dark" content="点赞" placement="bottom-end">
                                    <el-button type="warning" icon="Star" circle @click="star(image.image_tag_md5_id)"
                                        style="margin-left: 20px;" />
                                </el-tooltip>
                                <span :ref="'star_' + image.image_tag_md5_id">{{ image.starview }}</span>
                            </div>
                        </div>
                    </div>
                </el-card>
            </el-space>
        </el-col>
    </el-row>
    <el-row :gutter="16" v-show="showMore">
        <el-col :span="20" :offset="3">
            <el-button @mouseover="loadMore" type="primary"
                style="width:50vw;height:70px;cursor: pointer;">鼠标移到这里加载更多...</el-button>
        </el-col>
    </el-row>
</template>
  
<style scoped>
.deleteButton {
    margin-left: 4px;
    padding-top: 40;
    margin-top: -30px;
    position: absolute;
}

.shareButton {
    margin-left: 50px;
    padding-top: 40;
    margin-top: -30px;
    position: absolute;
}



.shadow {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    /* 原本的阴影样式 */
    transition: box-shadow 0.3s ease-in-out;
    /* 添加阴影时的过渡效果 */
}

.shadow:hover {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    /* 鼠标移动上去时的阴影样式 */
}

.infinite-list {
    height: 300px;
    padding: 0;
    margin: 0;
    list-style: none;
}

.infinite-list .infinite-list-item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
    background: var(--el-color-primary-light-9);
    margin: 10px;
    color: var(--el-color-primary);
}

.infinite-list .infinite-list-item+.list-item {
    margin-top: 10px;
}


.album-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.album-image {
    border-radius: 7px;
    margin-bottom: 10px;
    flex-basis: 25%;
}

.el-row {
    padding-top: 20px;
}

.time {
    font-size: 12px;
    color: #999;
}

.bottom {
    margin-left: -30px;
    margin-top: 13px;
    line-height: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button {
    padding: 0;
    min-height: auto;
}


.text-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
}

.card {
    display: flex;
    justify-content: center;
    align-items: center;
}

.card-content {
    text-align: center;
}
</style>
  
<script>

import { SERVER_DOMAIN } from '../Config.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
const IMAGE_GET_URL = SERVER_DOMAIN + "/api/readImage?id="

import { ref } from 'vue'
export default {
    data() {
        return {
            images: [
            ],
            url: '',
            sizeNum: 0,
            photos: {},
            count: ref(0),
            load: () => {
                this.count += 2
            },
            showMore: true,
            isStaring: false,
            isComing: false

        };
    },
    setup(props, { emit }) {

    },
    mounted: function () {
        this.loadPhotos(0)
        this.load()
    },
    created() {
        this.$bus1.on('addImagesList', (data) => {
            this.addImagesList(data.createImgData)
            // console.log("B接收到A的数据:", data)
        });

        this.$bus1.on('addImagesFirst', (data) => {
            this.addImagesFirst(data.createImgData)
            // console.log("B接收到A的数据:", data)
        });
    },
    methods: {
        load() {
            count.value += 2
        },
        handleImageError(error, src) {
            console.error(`Failed to load image: ${src}`);
        },
        addImagesFirst(imageData) {
            imageData.share = 0
            imageData.self = 1

            this.addImagesList(imageData) // 重用
            let lastItem = this.images.pop(); // 将最后一个元素弹出
            this.images.unshift(lastItem); // 将弹出的元素插入数组首位
        },
        addImagesList(imageData) {
            let strPrompt = "希望出现内容描述：" + imageData.prompt + ",不希望出现的内容:" + imageData.negative_prompt + ",采样迭代步数:" + imageData.step + ",高宽:" + imageData.sizeh + "X" + imageData.sizew + ",种子:" + imageData.seed
            let strPromptShort = imageData.prompt
            if (imageData.name != null && imageData.name != "" && imageData.name != undefined) {
                strPromptShort = imageData.name
            } else {
                strPromptShort = strPromptShort.substring(0, 100);
                strPromptShort += "...  "
            }
            imageData.url = IMAGE_GET_URL + imageData.image_tag_md5_id
            this.images.push({ url: imageData.url, seedid: imageData.image_tag_md5_id, seed: imageData.seed, strPromptShort: strPromptShort, starview: imageData.star, strPrompt: strPrompt, image_tag_md5_id: imageData.image_tag_md5_id, imageData: imageData })
            // let lastItem = this.images.pop(); // 将最后一个元素弹出
            // this.images.unshift(lastItem); // 将弹出的元素插入数组首位
        },
        imageAddList() {

        },
        copyPrompt(seedId) {
            const promptsText = this.$refs['prompts_' + seedId][0].innerHTML
            navigator.clipboard.writeText(promptsText).then(() => {
                this.$message.success(promptsText + '   \r\n\r\n\r\n                             已复制到剪切板');
            }, () => {
                this.$message.error('复制失败');
            });
        }, downloadImg(seedId) {
            const imageSrc = this.$refs['image_' + seedId][0].src + "&t=4"
            window.open(imageSrc, '_blank')
        },
        copyToInput(imageData) {
            //设置绘画描述
            this.$bus1.emit("setPromptInfo", { "prompt": imageData.prompt, "negativePrompt": imageData.negative_prompt });
            //设置高级
            this.$bus1.emit("setAdvancedInfo", { "seed": imageData.seed, "step": imageData.step, "imageBatchCount": 1, "imageBatchSize": 1 });
            //设置画幅
            this.$bus1.emit("setImageSize", { "width": imageData.sizew, "height": imageData.sizeh })
            //关闭随机
            this.$bus1.emit("setRandomPrompt", { "randomPrompt": false })

            this.$bus1.emit("setElCollapseExpand", {})
        },
        async loadPhotos(sizeNum) {
            if (this.isComing) {
                return
            }
            debugger
            this.isComing = true
            this.$myFetch('/api/photos', 'POST', { 'size': sizeNum })
                .then(result => {
                    if (result == null) {
                        return false
                    }
                    this.isComing = false
                    this.photos = result;
                    for (let i = 0; i < this.photos.rows.length; i++) {
                        console.log(this.photos.rows[i].url)
                        this.addImagesList(this.photos.rows[i])
                    }
                    if (this.photos.rows.length == 0) {
                        this.showMore = false
                        this.$message.warning('已经到底部了!!!');
                        this.$bus1.emit('setPageProgress', { pageNum: 1, totalSize: 1 });
                    } else {
                        this.$bus1.emit('setPageProgress', { pageNum: this.photos.pageNum, totalSize: this.photos.totalSize });
                    }
                })
        },
        loadMore() {
            let sizeNum = parseInt(this.photos.pageNum) + 10
            this.loadPhotos(sizeNum);
        }
        ,
        showImageDialog(data) {
            console.log(data)
            this.$bus1.emit("showImageDialog", {
                imageData: data
            });
        }, star(id) {
            this.$message.success('加油!!!');
            this.isStaring = true
            this.$myFetch('/api/star', 'POST', { id: id })
                .then((data) => {
                    this.isStaring = false
                    this.$refs['star_' + id][0].innerHTML = data.starNum
                })
                .catch(error => console.error(error));
        }, deleteImage(index, id, user_id) {
            this.$myFetch('/api/deleteImage', 'POST', { id: id })
                .then((data) => {
                    if (data.code == 200 && data.flag) {
                        this.images.splice(index, 1)
                        ElMessage({
                            showClose: true,
                            message: '删除成功.',
                            type: 'success',
                        })
                    } else {
                        ElMessage({
                            showClose: true,
                            message: '删除失败，可能你没有权限删除，这个作品属于：' + user_id,
                            type: 'error',
                        })
                    }
                })
                .catch(error =>
                    ElMessage({
                        showClose: true,
                        message: '删除失败,未知.',
                        type: 'error',
                    })
                );
        }, shareImageStatus(imgObj, flag) {
            debugger
            this.$myFetch('/api/share', 'POST', { id: imgObj.image_tag_md5_id, flag: flag })
                .then((data) => {
                    if (data.code == 200 && data.flag) {
                        if (data.flag) {
                            // 操作成功
                            if (flag == 1) {
                                // 共享成功
                                ElMessage({
                                    showClose: true,
                                    message: '共享成功，其他人都能看见你的作品并可进行点赞.',
                                    type: 'success',
                                })
                                imgObj.share = 1
                            } else {
                                // 取消共享成功
                                ElMessage({
                                    showClose: true,
                                    message: '取消成功，其他人将不能再看见你的作品，只有自己能看见.',
                                    type: 'success',
                                })

                                imgObj.share = 0
                            }
                        }
                    } else {
                        ElMessage({
                            showClose: true,
                            message: '失败，作品用户是：' + imgObj.user_id,
                            type: 'error',
                        })
                    }
                })
        }, confirmEvent(imgObj, flag) {
            shareImageStatus(imgObj, flag)
            console.log('confirm!')
        },
        cancelEvent() {
            console.log('cancel!')
        }
    }
}
</script>
  
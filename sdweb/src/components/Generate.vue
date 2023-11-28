<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <span class="demonstration" style="line-height: 30pt;">
        <el-button :type="createImagesBtnType" :size="large" :disabled="createImagesBtnDisabled" @Click="createSubmit"
            style="height: 50px;width: 150px;">{{
                createImagesBtnTxt }}</el-button>
    </span>
</template>

<script>
import { SERVER_DOMAIN } from '../Config.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const IMAGE_GET_URL = SERVER_DOMAIN + "/api/readImage?id="

let imgData = {
    prompt: '',
    negative_prompt: '',
    seed: 0,
    step: 0,
    imageBatchCount: 0,
    imageBatchSize: 0,
    sizew: 0,
    sizeh: 0,
    hires_upscale: 1
}
let selectModel = {}
export default {
    data() {
        return {
            createImagesBtnTxt: "开始生成",
            createImagesBtnType: "warning",
            createImagesBtnDisabled: false,
            createRunning: false,
            randomPrompt: true
        }
    },
    created() {
        this.$bus1.on('generateBtnReset', (data) => {
            this.resetButton()
        });
        this.$bus1.on('generateDialogToImages', (data) => {
            imgData.prompt = data.prompt
            this.createImages()
        });
    },
    setup(props) {
    },
    mounted: function () {

    }, methods: {
        createSubmit() {
            //检查
            this.$bus1.emit("getPromptInfo", (prompt, negative_prompt, randomPrompt) => {
                imgData.prompt = prompt
                imgData.negative_prompt = negative_prompt
                this.randomPrompt = randomPrompt
            });

            if (this.createRunning) {
                this.interrupt()
                return
            }
            if (this.randomPrompt) {
                //随机抽签模式
                this.$bus1.emit("showRandomTagDialog", {})
            } else {
                this.createImages()
            }

            // 检查随机开关开了没
        },
        interrupt() {

            this.createImagesBtnTxt = "停止中...",
                this.$myFetch('/api/interrupt', 'POST', null)
                    .then(result => {
                        this.resetButton();
                        this.$bus1.emit("generateDialogProcessDestroy");
                    })
        },
        createImages() {
            imgData = {}
            this.$bus1.emit("createSeedRandom", {})
            // 调用InputPrompt.vue中getPromptInfo  

            //调用Advanced vue中的getAdvancedInfo
            this.$bus1.emit("getAdvancedInfo", (seed, step, imageBatchCount, imageBatchSize,cfgScale,samplerIndex) => {
                imgData.seed = seed
                imgData.step = step
                imgData.imageBatchCount = imageBatchCount
                imgData.imageBatchSize = imageBatchSize
                imgData.cfgScale = cfgScale
                imgData.samplerIndex = samplerIndex
            });
            this.$bus1.emit("getImageSize", (w, h,upscaleB) => {
                imgData.sizew = w
                imgData.sizeh = h
                imgData.upscaleB = upscaleB
            });
            this.$bus1.emit("getPromptInfo", (prompt, negative_prompt, randomPrompt) => {
                imgData.prompt = prompt
                imgData.negative_prompt = negative_prompt
                this.randomPrompt = randomPrompt
            });


            //调用
            if (imgData.prompt == "" &&  this.randomPrompt) {
                ElMessageBox.alert('绘画内容描述中-希望出现的内容没有填写-No input prompt', '有内容没填写-No input prompt', {
                    // if you want to disable its autofocus
                    // autofocus: false,
                    confirmButtonText: 'OK',
                    callback: () => {
                        this.$bus1.emit("setElCollapseExpand", {})
                    }
                })
                return
            }

            this.createImgData = null
            if (this.seedRandomCheck) {
                this.seedNumMake()
            }
            this.createImagesBtnTxt = "Stop(终止)"
            this.createImagesBtnType = "info"
            this.createRunning = true

            this.$bus1.emit("getModelInfoSelected", function (model) {
                selectModel = model
            });
            if (selectModel != undefined && selectModel.title != "") {
                this.switchModel(selectModel.title)
            }
            this.$bus1.emit("generateDialogShowHidden", { show: true });
            this.$myFetch("/api/create", 'POST', imgData)
                .then((resultData) => {
                    //到这里不是运行状态说明被提前终止，这里就需要直接返回不再继续
                    if (this.createRunning == false) {
                        return
                    }
                    this.$bus1.emit("generateDialogProcessDestroy", {});
                    if (resultData.sub_seed_path.length == 1) {
                        //如果不是批量生成只有一个情况下
                        // imageB64 = "data:image/png;base64," + resultData[0].image
                    }
                    this.$bus1.emit("generateDialogDone", {
                        processCount: 100,
                        imageUrl: IMAGE_GET_URL + resultData.sub_seed_path[0].image_tag_md5_id + "&t=4"
                    });
                    for (let i = 0; i < resultData.sub_seed_path.length; i++) {
                        let imgurl = IMAGE_GET_URL + resultData.sub_seed_path[i].image_tag_md5_id + "&t=4"

                        this.$bus1.emit("generateDialogPushSrcList", {
                            imageUrl: imgurl
                        });
                        let imgDataNew = {}
                        Object.assign(imgDataNew, imgData);

                        imgDataNew["seed"] = resultData.seed
                        imgDataNew["image_tag_md5_id"] = resultData.sub_seed_path[i].image_tag_md5_id
                        imgDataNew["star"] = 0
                        this.$bus1.emit("addImagesFirst", {
                            createImgData: imgDataNew,
                            url: imgurl
                        });

                        if (resultData.seed != -200) {
                        }
                    }
                    this.resetButton();
                })
                .catch(error => {
                    this.resetButton();
                    this.$bus1.emit("generateDialogProcessDestroy");
                    console.log(error);
                    console.log("..................................................................");
                    this.$message.error('创建绘画失败,可能相关图画描述及种子图已存在,请查看历史生成图');
                });
        }
        , switchModel(modeName) {
            let model = { modelId: modeName }
            this.$myFetch(SERVER_DOMAIN + "/api/changeModel", 'POST', model)
                .then(result => {

                })
        },
        resetButton() {
            this.createImagesBtnTxt = "Generate(生成)"
            this.createImagesBtnType = "warning"
            this.createImagesBtnDisabled = false
            this.createRunning = false
        }
    }
}

</script>
<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-drawer v-model="createImageDialog" size="70%" title="正在生成中..." :direction="createImageDialogType">
        <span>请稍等..</span>
        <el-image style="width: 70%; height: 70%;" :src="generateImageSrc" :zoom-rate="1.7"
            :preview-src-list="generateImageSrcList" :initial-index="4" fit="contain">
            <template #error>
                <div class="image-slot">
                    <el-icon><icon-picture /></el-icon>
                </div>
            </template>
        </el-image>
        <el-progress class="progresscss" :percentage="processCount" :format="processTabFormat" />
        <el-button type="primary" style="margin-left: 16px;cursor: pointer;" @click="closeDialog"
            size="large">关闭</el-button>
    </el-drawer>
</template>
<style scoped>
.progresscss {
    width: 95vw;
    padding-left: 70px;
}
</style>
<script>
import { SERVER_DOMAIN } from '../Config.vue'


const processTabFormat = (percentage) => (percentage === 100 ? '完成' : `${percentage}%`)

//:before-close="handleCloseCreateImage"
const handleCloseCreateImage = (done) => {
    // ElMessageBox.confirm('Are1 you sure you want to close this?')
    //     .then(() => {
    //         done()
    //     })
    //     .catch(() => {
    //         // catch error
    //     })
}
export default {
    data() {
        return {
            createImageDialog: false,
            createImageDialogType: "ttb",
            handleCloseCreateImage: handleCloseCreateImage,
            processTabFormat: processTabFormat,
            processCount: 100,
            createImageCloseBtn: false,
            createRunning: false,
            generateImageSrc: "",
            generateImageSrcList: [],
            processTimer: null,
        }
    },
    created() {
    },
    setup(props) {
    },
    mounted: function () {
        this.$bus1.on('generateDialogShowHidden', (data) => {
            if (data.show) {
                this.createImageDialog = true
                this.processCount = 0
                this.processStart()
            } else {
                this.createImageDialog = false
                this.processDestroy()
            }
        });
        this.$bus1.on('generateDialogPushSrcList', (data) => {
            this.generateImageSrcList.push(data.imageUrl)  //多图像列表
        });

        this.$bus1.on('generateDialogDone', (data) => {
            this.processCount = data.processCount //进度
            this.generateImageSrc = data.imageUrl //最终生成图像
            // console.log(this.generateImageSrc)
        });
        this.$bus1.on('generateDialogProcessDestroy', (data) => {
            this.processDestroy()
        });



    }, methods: {
        processGet() {
            let data = {
                "id_task": "task(9frna2krmb6q5l9)",
                "id_live_preview": -1
            }
            if (this.createRunning) {
                return
            }

            this.createRunning = true
            this.$myFetch("/api/process", 'POST', null)
                .then((rtndata) => {
                    this.createRunning = false
                    // 活动中，循环检查
                    if (rtndata.eta_relative > 0) {
                        console.log("activeactiveactive")
                        this.processCount = parseInt(rtndata.progress * 100)
                        this.generateImageSrc = "data:image/png;base64," + rtndata.current_image
                    } else {
                        //沒活動 
                        this.processDestroy()
                    }
                })
                .catch(error => {
                    console.log(error);
                    this.processDestroy()
                });

        }, processStart() {
            this.generateImageSrcList = []
            this.generateImageSrc = ""
            this.processDestroy()
            this.processTimer = setInterval(() => {
                this.processGet();
            }, 1000);
        },
        processDestroy() {
            this.createRunning = false
            clearInterval(this.processTimer);
            this.processTimer = null
        },
        closeDialog() {
            this.createImageDialog = false
            this.processDestroy()
        }
    }
}
</script>


<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-row>
        <el-col :span="24" style="font-size:12px">
            <el-tooltip class="box-item" effect="dark" content="说出你想要画的内容，说的越详细图画越近似，可以通过拆成多个描述词以逗号分割进行描述"
                placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">图像比例</span>
            </el-tooltip>
            <div class="card-container">
                <div class="card" v-for="(card, index) in cards" :key="index" :class="{ 'selected': card.selected }"
                    @click="selectCard(index)">
                    <div class="inner-card">
                        <div class="inner-card-content"
                            :style="{ 'width': card.width + '%', 'height': card.height + '%', 'padding-top': '-50px' }">
                            <div class="inner-card-border"></div>
                            <div style="margin-top:-20px;text-align: center;"> {{ card.scale }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="10" :offset="1">
            <div style="margin-top:30px">
                <el-tooltip class="" effect="dark" content="说出你想要画的内容，说的越详细图画越近似，可以通过拆成多个描述词以逗号分割进行描述"
                    placement="top-start">
                    <span class="demonstration" style="line-height: 30pt;">宽</span>
                </el-tooltip>
                <span class="text-space">
                    <el-input-number v-model="width" :min="20" :max="2560" />
                </span>
                <div style="position: absolute;margin-top:-20px;margin-left:200px">
                    <el-tooltip class="box-item" effect="dark" content="开启高清修复需要消耗更多算力和时间，使用Latent 采样器"
                        placement="top-start">
                        <el-switch v-model="upscaleB" class="ml-2" inline-prompt size="large"
                            style="--el-switch-on-color:  #ff4949; --el-switch-off-color:#13ce66" active-text="高清修复"
                            inactive-text="原始大小" @change="switchUpscaleSize" />
                    </el-tooltip>
                </div>
            </div>

            <div style="">
                <el-tooltip class="" effect="dark" content="说出你想要画的内容，说的越详细图画越近似，可以通过拆成多个描述词以逗号分割进行描述"
                    placement="top-start">
                    <span class="demonstration" style="line-height: 30pt;">高</span>
                </el-tooltip>
                <span class="text-space">
                    <el-input-number v-model="height" :min="20" :max="2560" />
                </span>
            </div>
        </el-col>
    </el-row>
</template>
  
<script>

let sizew = 50
let sizeh = 50

export default {
    data() {
        return {
            width: 512,
            height: 512,
            upscaleB: false,
            cards: [
                { width: sizew * 1.5, height: sizeh * 1.5, scale: '1:1', selected: true },
                { width: sizew * 1 * 2.0, height: sizeh * (1 / 2) * 2.0, scale: '1:2', selected: false },
                { width: sizew * (4 / 3) * 1.2, height: sizeh * 1.2, scale: '4:3', selected: false },
                { width: sizew * (3 / 4) * 1.5, height: sizeh * 1.5, scale: '3:4', selected: false },
                { width: sizew * (16 / 9) * 1, height: sizeh * 1, scale: '16:9', selected: false },
                { width: sizew * (9 / 16) * 2, height: sizeh * 1.7, scale: '9:16', selected: false },
            ],
            selectedCardIndex: 0
        };
    },
    mounted: function () {
        this.setElCollapseShowImageSize()
    },
    created() {
        this.$bus1.on('getImageSize', (callback) => {
            callback(this.width, this.height,this.upscaleB)
        });
        this.$bus1.on('setImageSize', (data) => {
            this.width = data.width
            this.height = data.height
            this.setElCollapseShowImageSize()
        });
    },
    methods: {
        setElCollapseShowImageSize() {
            this.$bus1.emit("setElCollapseShowImageSize", {
                width: this.width, height: this.height
            });
        },
        selectCard(index) {
            this.selectedCardIndex = index;
            this.cards.forEach((card, i) => {
                card.selected = i === index;
            });
            this.setHeightWidth(1)
        },
        setHeightWidth() {
            let index = this.selectedCardIndex
            let h = 0
            let w = 0
            if (index == 0) {
                h = 512
                w = 512
            } else if (index == 1) {
                h = 512
                w = 768
            } else if (index == 2) {
                h = 512
                w = 683
            } else if (index == 3) {
                h = 683
                w = 512
            } else if (index == 4) {
                h = 288
                w = 512
            } else if (index == 5) {
                h = 512
                w = 288
            }

            if (this.upscaleB) {
                this.height = h * 2
                this.width = w * 2
            } else {
                this.height = h
                this.width = w
            }
            this.setElCollapseShowImageSize()
            console.log(this.width);
        }, switchUpscaleSize(b) {
            this.upscaleB = b
            this.setHeightWidth()
        }
    },
};
</script>
  
<style scoped>
.text-space {
    padding-left: 15px;
}

.table-header-fixed {
    position: sticky;
    top: 0;
    z-index: 1;
}

.card-container {
    display: flex;
    justify-content: space-between;
}

.card {
    width: 60px;
    height: 60px;
    border: 1px solid #898787;
    border-radius: 10%;
    position: relative;
}

.card.selected {
    cursor: pointer;
    border-color: rgb(240, 224, 240);
    background-image: linear-gradient(to right, rgba(236, 235, 235, 0.842), rgb(169, 210, 239), rgba(220, 216, 216, 0.872));
    background-position: center;
    background-size: cover;
    box-shadow: 0 0 0px 0px white;
}

.inner-card {
    border-radius: 10%;
    position: absolute;
    top: 14px;
    left: 5px;
    right: 5px;
    bottom: 5px;
    display: flex;
    align-items: center;
    justify-content: center;

}

.inner-card-content {
    position: relative;
    width: 100%;
    height: 100%;
}

.inner-card-border {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border: 3px dashed rgb(160, 13, 13);
}
</style>
  
<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template  >
    <el-row>
        <el-col :span="18" :offset="1">
            <el-tooltip class="box-item" effect="dark" content="每个描述词都对应无数种近似图片，图片种子是描述图片唯一编号，可以通过描述词+种子复现之前图片"
                placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">图片种子
                    <el-icon class="header-icon">
                        <info-filled />
                    </el-icon>
                </span>
                
            </el-tooltip>
            <div class="slider-demo-block">
                <el-input-number v-model="seed" value="3" :min=1 :max=10000000000 style="width:150px;text-align: left;"
                    @change="seedNumChange" />
                <el-tooltip class="box-item" effect="dark" content="每次生成换不同种子" placement="top-start">
                    <el-checkbox v-model="seedRandomCheck" style="margin-left:20px">每次随机种子</el-checkbox>
                </el-tooltip>
            </div>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="22" :offset="1">
            <!-- <div class="grid-content ep-bg-purple" /> -->
            <el-tooltip class="box-item" effect="dark" content="每个采样器都有自己独特的风格，有些采样器需要更多采样迭代步数才会出好片" placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">采样方法
                    <el-icon class="header-icon"><info-filled /></el-icon>
                </span>
            </el-tooltip>
            <el-select v-model="samplerIndex" placeholder="Select" style="width: 240px" @change="samplerChange">
                <el-option v-for="sampler in samplerIndexArr" :key="sampler" :label="sampler" :value="sampler" />
            </el-select>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="22" :offset="1">
            <!-- <div class="grid-content ep-bg-purple" /> -->
            <el-tooltip class="box-item" effect="dark" content="建议20，采样数越高细节越多，但生成速度越慢" placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">采样迭代步数
                    <el-icon class="header-icon"><info-filled /></el-icon></span>
            </el-tooltip>
            <el-slider v-model="step" show-input :min=1 :max=40 />
        </el-col>
    </el-row>

    <el-row>
        <el-col :span="22" :offset="1">
            <!-- <div class="grid-content ep-bg-purple" /> -->
            <el-tooltip class="box-item" effect="dark" content="提示词相关性Scale，是希望出现词和图像匹配度，值越大AI越自由发挥，值越小越和描述词匹配,推荐7。"
                placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">提示词相关性
                    <el-icon class="header-icon"><info-filled /></el-icon></span>
            </el-tooltip>
            <el-slider v-model="cfgScale" show-input :min=1 :max=40 />
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="22" :offset="1">
            <!-- <div class="grid-content ep-bg-purple" /> -->
            <el-tooltip class="box-item" effect="dark" content="每个批次生成的图片都不一样" placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">生成批次
                    <el-icon class="header-icon"><info-filled /></el-icon></span>
            </el-tooltip>
            <el-slider v-model="imageBatchCount" show-input :min=1 :max=20 />
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="22" :offset="1">
            <!-- <div class="grid-content ep-bg-purple" /> -->
            <el-tooltip class="box-item" effect="dark" content="每批次生成微调风格数量" placement="top-start">
                <span class="demonstration" style="line-height: 30pt;">每批次数量
                    <el-icon class="header-icon"><info-filled /></el-icon></span>
            </el-tooltip>
            <span class="demonstration">
                <el-tooltip class="box-item" effect="dark" content="Left Top prompts info" placement="top-start">
                </el-tooltip>
            </span>
            <el-slider v-model="imageBatchSize" show-input :min=1 :max=20 />
        </el-col>
    </el-row>
</template>


 
<script >
import { SERVER_DOMAIN } from '../Config.vue'
export default {
    data() {
        return {
            seed: -1,
            seedRandomCheck: true,
            imageBatchCount: 1,
            imageBatchSize: 1,
            step: 20,
            sizew: 0, //图片宽度
            sizeh: 0, //图片高度 
            cfgScale: 7,
            samplerIndexArr: ['Euler a'],
            samplerIndex: 'Euler a'
        };
    },
    created() {
        this.$bus1.on('getAdvancedInfo', (callback) => {
            this.getAdvancedInfo(callback)
        });

        this.$bus1.on('setAdvancedInfo', (data) => {
            this.setAdvancedInfo(data.seed, data.step, data.imageBatchCount, data.imageBatchSize, data.cfgScale, data.samplerIndex)
        });

        this.$bus1.on('createSeedRandom', (data) => {
            this.createSeedRandom()
        });


    },
    setup(props) {

    },
    mounted: function () {
        this.getSampler()
        this.seedNumMake()
    },
    methods: {
        setAdvancedInfo(seed, step, imageBatchCount, imageBatchSize, cfgScale, samplerIndex) {
            this.seed = seed
            this.step = step
            this.imageBatchCount = imageBatchCount
            this.imageBatchSize = imageBatchSize

            if (cfgScale == null || cfgScale == '') {
                cfgScale = 7
            }
            this.cfgScale = cfgScale

            if (samplerIndex == null || samplerIndex == '') {
                samplerIndex = 'Euler a'
            }
            this.samplerIndex = samplerIndex
        },
        getAdvancedInfo(callback) {
            callback(this.seed, this.step, this.imageBatchCount, this.imageBatchSize, this.cfgScale, this.samplerIndex)
        },

        randomNum(min, max) {
            return Math.floor(Math.random() * (max - min + 1) + min);
        },
        seedNumMake() {
            this.seed = this.randomNum(1000222, 9000000001)
            console.log(this.seed); // 输出随机数
        },
        seedNumChange(value) {
            this.seedRandomCheck = false
        },
        createSeedRandom() {
            if (this.seedRandomCheck) {
                this.seedNumMake()
            }
        },
        getSampler() {
            this.$myFetch(SERVER_DOMAIN + "/api/getSampler", 'POST', {})
                .then(result => {
                    if (result.length > 0) {
                        this.samplerIndexArr = result
                        let sampler = localStorage.getItem('samplerIndex')
                        if (sampler == null || sampler == "") {
                            sampler = 'Euler a'
                        }
                        this.samplerIndex = sampler
                    }
                })
        },
        samplerChange(val) {
            this.samplerIndex = val
            localStorage.setItem('samplerIndex', val)
        }
    },
    render() {
    },
};


</script>
<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-dialog v-model="imgageShowDialogVisible" title="图片预览" width="85vw" center>
        <div>
            <el-container>
                <el-aside class="imgageShowDialogBox">
                    <el-image name="test" lazy class="album-image shadow"
                        style="height: calc(100% - 60px); cursor: pointer; user-select: none; box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);border-radius: 2%;"
                        :src="imageurl" :zoom-rate="0.4" :initial-index="1" fit="cover" :hide-on-click-modal="true"
                        :z-index="22" />
                </el-aside>
                <el-main class="imgageShowDialogBox2">
                    <div class="imgageShowDialogDiv">
                        图片名称/备注:
                    </div>
                    <div id="">
                        {{ name }}
                    </div>
                    <div class="imgageShowDialogDiv">
                        希望出现的(prompt):
                    </div>
                    <div>
                        {{ prompt }}
                    </div>
                    <div class="imgageShowDialogDiv">
                        不希望出现的(negative prompt):
                    </div>
                    <div>
                        {{ negative_prompt }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        图片大小高x宽(Size):
                    </div>
                    <div>
                        {{ size }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        图片种子(Seed):
                    </div>
                    <div>
                        {{ seed }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        放大(Upscale):
                    </div>
                    <div>
                        {{ upscale }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        采样迭代步数(Step):
                    </div>
                    <div>
                        {{ step }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        Eta:
                    </div>
                    <div>
                        {{ eta }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        降噪强度(denoising strength):
                    </div>
                    <div>
                        {{ denoising_strength }}
                    </div>

                    <div class="imgageShowDialogDiv">
                        创作者:
                    </div>
                    <div>
                       {{ user_id }} ({{create_ip }})
                    </div>
                    
                </el-main>
            </el-container>
        </div>
    </el-dialog>
</template>
<script lang="ts" >
import { ref } from 'vue'


export default {
    data() {
        return {
            name: '',
            prompt: '',
            negative_prompt: '',
            size: '',
            seed: '',
            upscale: '',
            step: '',
            eta: '',
            denoising_strength: '',
            imageurl: '',
            imgageShowDialogVisible: ref(false),
            create_ip:'',
            user_id:''
        };
    },
    setup(props, { emit }) {

    },
    created() {
        this.$bus1.on('showImageDialog', (data) => {
            this.showImageDialog(data)
        });
    },
    methods: {
        showImageDialog(data) {
            // imageData = 
            
            this.name = data.imageData.name
            this.prompt = data.imageData.prompt
            this.negative_prompt = data.imageData.negative_prompt
            this.size = data.imageData.sizeh + "x" + data.imageData.sizew
            this.prompt = data.imageData.prompt
            this.seed = data.imageData.seed
            this.upscale = data.imageData.hires_upscaler + "   倍数(" + data.imageData.hires_upscale + ")"
            this.step = data.imageData.step
            this.eta = data.imageData.eta
            this.denoising_strength = data.imageData.denoising_strength
            this.imageurl = data.imageData.url + "&t=4"
            this.imgageShowDialogVisible = true
            this.create_ip = data.imageData.create_ip
            this.user_id = data.imageData.user_id
            debugger
            
        }
    }
}




</script>
<style scoped>
.imgageShowDialogDiv {
    margin-top: 15px
}

.el-main {
    height: 70vh
}

.imgageShowDialogBox {
    width: 40vw;
    color: #854040;
    border-radius: 20px;
    border: 2px dashed #ccc;
    background-color: #f2f2f2;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 30px;
    text-align: center;
    align-items: center;
    justify-content: center;
}

.imgageShowDialogBox2 {
    margin-left: 20px;
    border-radius: 10px;
    color: #854040;
    border: 2px dashed #ccc;
    background-color: #f2f2f2;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 10px;

    word-wrap: break-word;
    word-break: break-all;
}

.el-dialog__body {
    color: #854040;
}</style>
  
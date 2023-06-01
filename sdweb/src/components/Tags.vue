<!-- https://github.com/newlxj/sdweb-multi-user-website for newlxj -->
<template>
    <el-row :gutter="16">
        <el-col :span="12" :offset="3">
            <el-select v-model="selectId" placeholder="Select" style="width: 240px" @change="tagsChange">
                <el-option v-for="(item, index) in tagsArray" :key="item.image_name" :label="item.image_name"
                    :value="index" />
            </el-select>
            <el-tooltip class="box-item" effect="dark" content="随机抽个模板" placement="right">
                <el-button type="primary" circle @click="randomX()" style="margin-left: 20px;">
                    <el-icon style="vertical-align: middle;">
                        <Refresh />
                    </el-icon>
                </el-button>
            </el-tooltip>
        </el-col>
    </el-row>
</template>

<script>



let tagsArray = []

tagsArray.push({
    image_name: "选择模板",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "",
    negative_prompt: "",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0

})

tagsArray.push({
    image_name: "红发少女，在樱花下",
    seed: 1033881260,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "eromanga,(loli:1.5),(extremely detailed CG unity 8k wallpaper,masterpiece, best quality, ultra-detailed), (best illumination, best shadow, an extremely delicate and beautiful), dynamic angle, floating, finely detail, Depth of field (bloom), (shine), glinting stars,(watercolor_medium), (painting), (sketch),white and pink wet hanfu| pajamas, pink thighhighs,keep hands on the back, smile, look at viewer, sakura and Jasmine background, long_flowing_hair, Jasmine Petals white hair, hair between wet breasts, sakura hair bow, highly detailed, high resolution, cinematic lighting, highly detailed eyes, (solo), game_cg,1girl, Princess, bangs, blue sakura, detailed_foreground, blush, medium breasts, cherry_blossoms, eyebrows_visible_through_hair, falling_petals, floating_hair, sakura, hair_flower, hair_ornament, leaves_in_wind, long_hair, long_sleeves, looking_at_viewer, sakura petals,sakura petals_on_liquid, pink sakura flower, pink_hair, rose_petals, see-through, solo, spring_(season), upper_body, very_long_hair, wind, blue and red eyes,torino",
    negative_prompt: "(((simple background))),ugly,lowres, bad anatomy,worst quality, low quality, normal quality, [:((No more than one thumb, index finger, middle finger, ring finger and little finger on one hand),(mutated hands and fingers:1.5 ), fused ears, one hand with more than 5 fingers, one hand with less than 5 fingers,):0.5],bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, Missing limbs, three arms, bad feet, text font ui,signature, blurry, malformed hands, long neck, mutated hands and fingers :1.5). (long body :1.3),(mutation ,poorly drawn :1.2), disfigured, malformed, mutated, multiple breasts, futa, yaoi, three legs, huge breasts",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0
})

tagsArray.push({
    image_name: "白发猫耳朵少女",
    seed: 5124152700,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "((masterpiece)), ((an extremely detailed and delicate)), (8k cg wallpaper), (stunning art), ((illustration )), (ink splashing), color splashing, (amazing),original,(extremely fine and beautiful),photorealistic, (beautiful and clear background:1.25), (depth of field:0.7), (1 cute girl with (cat ear and cat tail:1.2) bathing in the garden,Tachibana Kanade:1.1), (cute:1.35), (detailed beautiful red eyes:1.3), (beautiful face:1.3), , silver hair, silver ear, (blue hair:0.8), (blue ear:0.8), long hair, wet see-through flowers texture lace clothes, hair blowing with the wind, (red eye:1.2), flowers fill the screen,fill the screen,butterflies flying around,smile",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0

})



tagsArray.push({
    image_name: "韩国女孩漫画",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "kyoto girl,loli",
    negative_prompt: "lowres,bad anatomy,bad hands,text,error,missing fingers,extra digit,fewer digits,cropped,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,username,blurry,bad feet,",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0

})

tagsArray.push({
    image_name: "可爱风格1",
    seedNum: -1,
    stepNum: 20,
    enlargeX: 1,
    tpblwidth: 512,
    tpblheight: 512,
    promptTxt: "masterpiece, best quality, kawaii,adorable girl,little girl,bishoujo,cute,very long hair,light brown hair,hair between eyes,ahoge, blue eyes,beautiful detailed eyes,aqua eyes,cat_ears,blue hairbow,white kneehighs,white dress,white infrared sleeve,((beautiful detailed face)), (beautiful detailed eyes),(loli),boots,full body,white glove,cute face,happy",
    negativepromptTxt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)"
})

tagsArray.push({
    image_name: "樱花少女",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "eromanga,(loli:1.5),masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper, multiple_girls,white and pink wet hanfu pajamas, pink thighhighs,keep hands on the back, smile, Princess,  look at viewer, sakura and Jasmine background, absurdly long hair, Jasmine Petals white hair, hair between wet breasts, sakura hair bow,  highly detailed, high resolution, cinematic lighting, highly detailed eyes, (solo), game_cg,1girl, bangs, blue sakura, blurry, blurry_foreground, blush, medium breasts, cherry_blossoms,  depth_of_field,eyebrows_visible_through_hair, falling_petals, floating_hair, sakura, hair_flower, hair_ornament, leaves_in_wind, long_hair, long_sleeves, looking_at_viewer, sakura petals,sakura petals_on_liquid, pink sakura flower, pink_hair, rose_petals, see-through,  solo, spring_(season), upper_body, very_long_hair,  wind, blue and red eyes,",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0

})
tagsArray.push({
    image_name: "小雪人",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "(absurdres:1.2), ((masterpiece)), ((ultra-detailed)), ((illustration)), (no humans:1.5), snowman, many snowman, multiple snowman, (blush stickers:1.3), (single color eyes), (simple eyes), white snowman, winter, snow, outdoor, tree",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0

})

tagsArray.push({
    image_name: "蓝色头发猫耳女孩",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: "((masterpiece)), ((an extremely detailed and delicate)), (8k cg wallpaper), (stunning art), ((illustration )), (ink splashing), color splashing, (amazing),original,(extremely fine and beautiful),photorealistic, (beautiful and clear background:1.25), (depth of field:0.7), (1 cute girl with (cat ear and cat tail:1.2) bathing in the garden:1.1), (cute:1.35), (detailed beautiful eyes:1.3), (beautiful face:1.3), (bare shoulder:1.5),ð, silver hair, silver ear, (blue hair:0.8), (blue ear:0.8), long hair, wet see-through flowers texture lace clothes, hair blowing with the wind, (blue eye:1.2), flowers fill the screen,fill the screen, (little girl:0.65),butterflies flying around",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0
})

tagsArray.push({
    image_name: "红眼睛的猫娘",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: " (masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper),kawaii, Round white eyebrows,night, night, artbook, highres, little girl, ((chibi)), (hair over shoulder), white hair, (ahoge), (embarrassed ), (blush), (cat_ears), (wide eyed), (slit pupils ), ((fangs)), (red eyes), (medium breasts), (japanese_clothes), halo, (looking up),",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0
})

tagsArray.push({
    image_name: "红眼睛的猫娘",
    seed: -1,
    step: 20,
    enlargeX: 1,
    sizew: 512,
    sizeh: 512,
    prompt: " (masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper),kawaii, Round white eyebrows,night, night, artbook, highres, little girl, ((chibi)), (hair over shoulder), white hair, (ahoge), (embarrassed ), (blush), (cat_ears), (wide eyed), (slit pupils ), ((fangs)), (red eyes), (medium breasts), (japanese_clothes), halo, (looking up),",
    negative_prompt: "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, bad feet,(bad hands),(bad breasts)",
    hires_upscale: "1",
    hires_upscaler: "",
    denoising_strength: 0.0
})


export default {
    data() {
        return {
            tagsArray: tagsArray,
            selectId: 0,
            images: [
            ],
            url: ''


        };
    },
    setup(props, { emit }) {

    },
    created() {
        // this.$bus1.on('addImagesList', (data) => {
        //     this.addImagesList(data.createImgData, data.imageUrl)
        //     // console.log("B接收到A的数据:", data)
        // });
        // // ref.$on('eventName', this.addRow);
        // // bus.on("ttt", this.addRow)
    },
    methods: {
        randomX() {
            let r = Math.floor(Math.random() * tagsArray.length) + 1
            this.selectId = r - 1
            this.$bus1.emit("setTagInfo", tagsArray[r - 1]);
        },
        tagsChange(value) {
            this.$bus1.emit("setTagInfo", tagsArray[value]);
        }
    }
}

// data.seedNum, data.stepNum, data.enlargeX, data.tpblwidth, data.tpblheight, data.promptTxt, data.negativepromptTxt





// this.$bus1.emit("setPromptInfo", {
//     seedNum: -1,
//     stepNum: 20,
//     enlargeX: ,
//     tpblwidth: ,
//     tpblheight: ,
//     promptTxt: ,
//     negativepromptTxt:
// });

</script>
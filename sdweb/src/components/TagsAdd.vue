<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-tag v-for="(tag, index) in tags" :key="index" closable @close="removeTag(index)" @click="editTag(index)"
        :style="tagStyle">
        {{ tag }}
    </el-tag>
    <br />
    <el-input v-model="newTag" placeholder="请输入标签名称" style="width: 150px;" :autosize="{ minRows: 1, maxRows: 10 }"
        type="textarea" ref="tagInput" :size="50"></el-input>
    <el-button type="primary" @click="submitTags">{{ buttonText }}</el-button>
</template>
    
<script>
import axios from 'axios'

import { SERVER_DOMAIN } from '../Config.vue'

export default {
    props: {
        Tagstr: {
            type: String,
            required: true
        }
    },
    computed: {
        tagStyle() {
            return {
                fontSize: '16px',
                margin: '2px 3px'
            };
        }
    },
    data() {
        return {
            tags: [],
            newTag: '',
            editIndex: -1,
            buttonText: '添加标签'
        }
    },
    mounted() {
        this.tags = this.Tagstr.split(",")
        console.log(this.Tagstr);
    },
    watch: {
        Tagstr(ntag, otag) {
            if (ntag != otag) {
                this.tags = this.Tagstr.split(",")
            }
        }
        // ,
        // tags(ntag, otag) {
        //     if (ntag != otag) {
        //         this.Tagstr = this.tags.join(', ');
        //     }
        // }
    },
    methods: {
        addTag() {
            if (this.newTag && !this.tags.includes(this.newTag)) {
                this.tags.push(this.newTag);
                this.newTag = '';
            }
        },
        removeTag(index) {
            this.tags.splice(index, 1);
        },
        editTag(index) {
            this.editIndex = index;
            this.newTag = this.tags[index];
            this.buttonText = '保存修改';
            this.$nextTick(() => {
                this.$refs.tagInput.focus();
            });
        },
        submitTags() {
            if (this.editIndex !== -1) {
                this.tags.splice(this.editIndex, 1, this.newTag);
                this.editIndex = -1;
                this.newTag = '';
                this.buttonText = '添加标签';
            } else {
                this.addTag();
            }
        }, getNewTags() {
            return this.tags.join(', ');
        }
    }
}
</script>
    
<style scoped>
.card-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.card-item {
    width: calc(33.3% - 10px);
    margin-bottom: 20px;
    cursor: pointer;
}

.el-input__count-inner {
    z-index: 1;
}

.el-tag {
    padding: 4px 8px;
}

.el-tag-clicked {
    background-color: orange;
}

.el-tag:hover {
    background-color: pink;
}
</style>
    
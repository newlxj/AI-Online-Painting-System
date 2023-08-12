<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
  <div>
    <!-- <el-button type="primary" @click="showDialog">打开对话框</el-button> -->
    <el-dialog v-model="dialogVisible" title="随机抽签" width="80%">
      本tag来自<a href="https://aitag.top" target="_blank">aitag.top</a>
      <div class="card-container">
        <el-card v-for="(item, index) in tableData" :key="index" class="card-item" :body-style="{ padding: '20px' }"
          :style="{ border: item.selected ? '2px solid #9b4dca' : '2px solid #ebeef5' }"
          @click.native="selectCard(index)">
          <p>

            <TagsAdd :Tagstr="item.name" ref="randomTagcard" />
            <!-- <el-input v-model="item.name" :autosize="{ minRows: 4, maxRows: 7 }" type="textarea"
              placeholder="Please input" show-word-limit maxlength="1500" :style="{ 'font-size': '16px' }" /> -->
          </p>
          <p>{{ item.desc }}</p>
          <img :src="item.image_md5_id" style="width: 100%">
        </el-card>
      </div>
      <el-tooltip class="box-item" effect="dark" content="如果图片中出现不想要的内容，在此指出哪里有问题，比如手有问题说手坏了，人物没有头发，说没有头发"
        placement="top-start">
        <span class="demonstration" style="line-height: 30pt;">不希望出现的内容</span>
      </el-tooltip>
      <div class="slider-demo-block">
        <el-input :autosize="{ minRows: 2, maxRows: 6 }" v-model="negative_prompt" maxlength="1500"
          placeholder="描述图片中不希望出现的内容，多个词用逗号分隔，比如手坏了，眼睛坏了，英文表示比如：bad hands,bad eyes" show-word-limit type="textarea" />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <div style="text-align: right; margin-top: 20px">
            <el-button type="primary" @click="refresh">换一组</el-button>
            <el-button type="primary" @click="submit">生成图像</el-button>
          </div>
        </span>
      </template>
    </el-dialog>

  </div>
</template>
  
<script>
import axios from 'axios'

import { DEFAULT_NAGATIVE_PROMPT } from '../Config.vue'
import TagsAdd from '../components/TagsAdd.vue'

export default {
  components: {
    TagsAdd
  },
  data() {
    return {
      dialogVisible: false,
      selectedCard: 0, 
      tableData: [],
      negative_prompt: DEFAULT_NAGATIVE_PROMPT
    }
  },
  created() {
    this.$bus1.on('showRandomTagDialog', (callback) => {
      this.showDialog()
    });
  },
  methods: {
    showDialog() {
      this.dialogVisible = true
      this.refresh()
      npstr = localStorage.getItem('negative_prompt')
      if (npstr != null && npstr != undefined) {
        this.negative_prompt = npstr
      }
    },
    refresh() {
      this.$myFetch('/api/getTag', 'POST', null)
        .then(response => {
          this.tableData = response.map(item => {
            return {
              name: item.name,
              desc: item.desc,
              image_md5_id: item.image_md5_id,
              selected: false
            }
          })
        })
        .catch(error => {
          console.log(error)
        })
    },
    selectCard(index) {
      this.selectedCard = index
      this.tableData.forEach((item, i) => {
        item.selected = i === index;
      });
    },
    submit() {
      const selectedCards = this.tableData.filter(item => item.selected)
      const selectName = selectedCards.map(item => item.name)
      if (selectName != null && selectName != "") {
        const newTags = this.$refs["randomTagcard"][this.selectedCard].getNewTags();
        this.dialogVisible = false
        localStorage.setItem('negative_prompt', this.negative_prompt)
        // 本地存储一份
        // this.$refs.child.childMethod();
        this.$bus1.emit("setPromptInfo", { prompt: newTags, negativePrompt: this.negative_prompt });
        this.$bus1.emit("generateDialogToImages", {});
      } else {
        this.$message.warning('注意，您没选抽签内容，请点击3个选项卡空白处选择一个进行生成，\n如果希望手写关键词请关闭随机抽签!!!');
      }
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
</style>
  
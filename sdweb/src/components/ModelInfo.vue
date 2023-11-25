<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-tooltip class="box-item" effect="dark" content="说出你想要画的内容，说的越详细图画越近似，可以通过拆成多个描述词以逗号分割进行描述" placement="top-start">
        <span class="demonstration" style="line-height: 30pt;">绘画风格{{ cardSelectTitle }}</span>
    </el-tooltip>
    <div class="card-container">
        <el-space style="text-align: center;margin-left: 10px;margin-bottom: 10px;">
            <el-card v-for="(item, index) in cardList.slice(0, 2)" :key="index" :class="{ 'selected': item.selected }"
                @click="selectCard(index)">
                <div
                    :style="{ 'background-image': `url(${serverAddr}/api/getModelImg?mid=${item.number})`, 'background-size': 'cover', 'width': '100px', 'height': '50px' }">
                </div>
                <div class="card-content" v-if="!item.selected">
                </div>
                <span class="card-title">{{ item.showName }}</span>
            </el-card>
        </el-space>
    </div>
    <span v-if="cardList.length > 2">
        <el-collapse :gutter="16" v-model="conllapseExpand">
            <el-collapse-item title="更多绘画风格" name ="1">
                <div class="card-container">
                    <el-space wrap :size="16">
                        <el-card v-for="(item, index) in cardList.slice(2, 99)" :key="index"
                            :class="{ 'selected': item.selected }" @click="selectCard(index + 2)">
                            <div
                                :style="{ 'background-image': `url(${serverAddr}/api/getModelImg?mid=${item.number})`, 'background-size': 'cover', 'width': '100px', 'height': '50px' }">
                            </div>
                            <div class="card-content" v-if="!item.selected">
                            </div>
                            <span class="card-title">{{ item.showName }}</span>
                        </el-card>
                    </el-space>
                </div>
            </el-collapse-item>
        </el-collapse>
    </span>
    <el-drawer :append-to-body="true" :visible.sync="false" :modal-append-to-body="false"
        v-model="dialogModelSettingVisible" title="设置模型" size="600" :direction="createImageDialogType">
        <!-- Drawer 内容 -->
        <div>
            <!-- 主要内容 -->
            <el-table :data="modelGridData" @selection-change="handleSelectionChange" :default-selection="defaultSelection"
                header-row-class-name="table-header-fixed">
                <el-table-column property="title" label="标题" />
                <el-table-column property="showName" label="显示名称" width="200px">
                    <template #default="scope">
                        <el-input v-model="scope.row.showName" autosize type="textarea" placeholder="输入显示名称(10个字内)" />
                    </template>
                </el-table-column>
                <el-table-column property="miniLogo" label="logo" width="200px">
                    <template #default="scope">
                        <el-input v-model="scope.row.miniLogo" autosize type="textarea"
                            placeholder="模型Logo存储位置(程序运行目录下位置，例如/modellogo/anax.png),宽100px 高50px" />
                    </template>
                </el-table-column>
                <el-table-column property="order" label="排序" width="60px">
                    <template #default="scope">
                        <el-input v-model="scope.row.order" placeholder="排序" />
                    </template>
                </el-table-column>
                <el-table-column property="desc" label="备注" width="200px">
                    <template #default="scope">
                        <el-input v-model="scope.row.desc" autosize type="textarea" placeholder="备注描述" />
                    </template>
                </el-table-column>
                <el-table-column label="绑定" width="100px">
                    <template #default="scope">
                        <el-checkbox v-model="scope.row.selectedx" />
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="btn-wrapper">
            <el-button @click="save" type="primary">保存</el-button>

        </div>
        <template #footer>
            <!-- footer-slot，用于放置底部固定按钮 -->
            <el-button>取消</el-button>
        </template>



    </el-drawer>
</template>
  
<script>
import { SERVER_DOMAIN } from '../Config.vue'

export default {
    data() {
        return {
            cardList: [],
            modelGridData: [],
            conllapseExpand: ['1'],
            dialogModelSettingVisible: false,
            selectedRows: [],
            defaultSelection: [],
            saveData: [],
            serverAddr: SERVER_DOMAIN,
            cardSelectTitle: '',
            createImageDialogType: "ttb",
            selectModel: {
                miniLogo: "",
                desc: "",
                number: 1,
                selectedx: false,
                showName: "",
                title: "",
                order: 1
            }
        };
    },
    mounted: function () {
        this.initAllModel()
        document.addEventListener('keydown', (event) => {
            if (event.altKey && event.code === 'KeyP') {
                this.selectCardAdvance()
                console.log('hello');
            }
        });

    },
    created() {
        this.$bus1.on('getModelInfoSelected', (callback) => {
            callback(this.selectModel)
        });
    },
    methods: {
        initAllModel() {
            this.$myFetch('/api/getCheckModelList', 'POST', null)
                .then((data) => {
                    this.cardList = this.orderList(data)
                })
                .catch(error => console.error(error));
        },
        selectCard(index) {
            this.cardList.forEach((item, i) => {
                item.selected = i === index;
                if (item.selected) {
                    this.selectModel = item
                    this.cardSelectTitle = "(" + item.showName + ")"
                    console.log(item);
                }
            });
        },

        selectCardAdvance() {
            this.$myFetch("/api/listModel", 'POST', null)
                .then(result => {
                    this.dialogModelSettingVisible = true
                    this.modelGridData = this.orderList(result)
                })
        },
        orderList(list) {
            return list.sort((a, b) => {
                if (a.order === '' && b.order === '') {
                    return 0;
                } else if (a.order === '') {
                    return 1;
                } else if (b.order === '') {
                    return -1;
                } else {
                    return parseInt(a.order) - parseInt(b.order);
                }
            });
        },
        save() {
            this.saveData = []
            const updatedRows = this.modelGridData.filter(row => row.title)
            let countRow = 0
            for (let row of updatedRows) {
                if (row.selectedx) {
                    countRow++
                    if (row.showName === undefined || row.showName === "") {
                        this.$message.error('请填写绑定值的显示名称')
                        return
                    }
                    if (row.desc === undefined || row.desc === "") {
                        row.desc = ""
                    }

                    if (row.miniLogo === undefined || row.miniLogo === "") {
                        row.miniLogo = ""
                    }
                    row.number = "" + countRow + ""
                    this.saveData.push(row)
                }
            }
            if (this.saveData.length === 0) {
                this.$message.error('请勾选需要绑定的模型')
                return
            }

            console.log(this.saveData)
            this.$myFetch('/api/saveSdModel', 'POST', this.saveData)
                .then((data) => {
                    this.dialogModelSettingVisible = false
                    this.$message.success("保存成功")
                    this.initAllModel()
                    console.log(data)
                })
                .catch(error => console.error(error));

            // fetch(SERVER_DOMAIN + "/api/saveSdModel", {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json'
            //     },
            //     body: JSON.stringify(this.saveData)
            // })
            //     .then(response => response.json())
            //     .then((data) => {
            //         this.dialogModelSettingVisible = false
            //         this.$message.success("保存成功")
            //         this.initAllModel()
            //         console.log(data)
            //     })
            //     .catch(error => console.error(error));

            // 批量保存操作
        },
        handleSelectionChange(selection) {
            // 将当前勾选的行数据保存在 selectedRows 数组中
            this.selectedRows = selection
        }
    },
};
</script>
  
<style scoped>
.btn-wrapper {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.12), 0 -1px 10px rgba(0, 0, 0, 0.08);
}

.btn-wrapper button {
    display: inline-block;
    vertical-align: middle;
    margin-right: 20px;
}

.el-drawer__body {
    overflow: auto;
}

.el-drawer__container ::-webkit-scrollbar {
    display: none;
}

.drawerCs {
    height: 700px;
}

.fonttext {
    font-size: 14px;
    color: #fff;
}

.card-container {
    display: flex;
    justify-content: space-between;
    margin: 0 auto;
}

.el-card {
    width: 100px;
    height: 100px;
    border-radius: 10px;
    text-align: center;
    --el-card-padding: 0px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
    border: 2px solid rgba(232, 232, 232, 0);
}

.el-card.selected {
    border: 2px solid purple;

}

.el-card.selected:hover {
    border: 2px solid purple;
}

.card-title {
    word-wrap: break-word;
    padding-top: 15px;
    font-size: 12px;
}

.card-content {

    display: none;
    align-items: top;
    justify-content: top;
    height: 100%;
    color: #fff;
    font-size: 14px;
}
</style>
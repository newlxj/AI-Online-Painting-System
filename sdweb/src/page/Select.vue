<!-- https://github.com/newlxj/sdweb-multi-user-website for newlxj -->
<script setup>
import Login from '../page/Login.vue'
</script >
<template>
    <Login />
    <div>
        <el-row>
            <el-col :span="8">
                <el-card class="mode-card card-hover" @click="gotoCreateMode" :class="{ 'card-grey': gotoCreateModeClick }">
                    <div class="mode-title">创造模式</div>
                    <div class="mode-desc">自己创造想要的图像（建议PC端使用）</div>
                </el-card>
                <el-card class="mode-card card-hover" @click="gotoBrushMode" :class="{ 'card-grey': gotoBrushModeClick }">
                    <div class="mode-title">刷图模式</div>
                    <div class="mode-desc">适合移动端刷图玩</div>
                </el-card>
                当前服务器状态：<el-tag :type='isOnline ? "success" : "error"'> {{ isOnlineMsg }} </el-tag>{{ isOnline ?
                    '尽情进行你的创作' : '浏览你的历史创作' }}

                <p>本站系统已在github开源</p>
                <p>当前平台共创作{{ allImageCount }}张杰作，期待你的创作及与大家分享</p>
                <p>4090免费算力平台</p>
                <p v-if="userid != '' && userid != null">当前登录账号{{ userid }} <el-button type="danger"
                        @click="logout">退出</el-button></p>
            </el-col>
            <el-col :span="2">
                <div class="bgimg"></div>
            </el-col>
        </el-row>

    </div>
</template >

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { SERVER_DOMAIN } from '../Config.vue'


export default {
    created() {
        this.check()
        this.$bus1.on('SelectPageRefresh', (callback) => {
            this.userid = localStorage.getItem('userid')
            this.showLoginInfo = true
            this.check()
        });
    },
    data() {
        return {
            isOnline: false,
            isOnlineMsg: '检测中...',
            gotoCreateModeClick: false,
            gotoBrushModeClick: false,
            userid: localStorage.getItem('userid'),
            allImageCount: 0,
            showLoginInfo: false
        }
    },
    mounted: function () {

    },
    methods: {
        gotoCreateMode() {
            if (this.isOnline) {
                this.$router.push('/createModel')
                this.gotoCreateModeClick = true
            } else {
                this.$message.error('服务器离线，请联系管理员，或使用刷图模式');
            }
        },
        gotoBrushMode() {
            this.$router.push('/viewer')
            this.gotoBrushModeClick = true
        },
        check() {
            this.$myFetch(SERVER_DOMAIN + '/api/checkx','POST')
                .then(data => {
                    if (data.warring != "") {
                        ElMessageBox.alert(data.warring, '使用警告', {
                            // if you want to disable its autofocus
                            // autofocus: false,
                            confirmButtonText: '我同意及希望继续使用',
                            showClose: false,
                            type: 'warning',
                            callback: () => {
                                // this.$bus1.emit("setElCollapseExpand", {})
                            }
                        })
                    }
                    this.allImageCount = data.imgCount
                    if (data.ol == 1) {
                        this.isOnline = true
                        this.isOnlineMsg = '在线'
                    } else {
                        this.isOnline = false
                        this.isOnlineMsg = '离线(' + data.offline + '分钟)'
                    }
                }).catch(error => {
                    // handle error
                })
        }, logout() {
            this.$cookies.remove("token")
            localStorage.removeItem("userid")
            window.location.reload()
        }
    }
}
</script>
  
<style scoped>
.bgimg {
    background-image: url('../assets/bg.jpg');
    background-size: 110% 100%;
    width: 800px;
    height: 600px;
    display: block;
    opacity: 0.2;
    z-index: -20;
}

.card-hover:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.mode-card {
    width: 400px;
    height: 200px;
    margin: 30px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.card-grey {
    background-color: #8aff94e3;
    border-color: #e4e7ed;
    color: #272827;
}

.mode-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}

.mode-desc {
    font-size: 16px;
    color: #999;
    text-align: center;
}
</style>
  
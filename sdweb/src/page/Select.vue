<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<script setup>
import Login from '../page/Login.vue'
</script >
<template>
  <div class="container">
    <Login />
    <div class="content">
      <el-row justify="center" align="middle">
        <el-col :span="24">
          <!-- 创造模式和刷图模式卡片 -->
          <el-card class="mode-card card-hover" style="margin: auto;" @click="gotoCreateMode" :class="{ 'card-grey': gotoCreateModeClick }">
            <div class="mode-title">画图模式</div>
            <div class="mode-desc">建议PC端使用</div>
          </el-card>
          <el-card class="mode-card card-hover" style="margin: auto;" @click="gotoBrushMode" :class="{ 'card-grey': gotoCreateModeClick }">
            <div class="mode-title">刷图模式</div>
            <div class="mode-desc">适合移动端刷图玩</div>
          </el-card>
          <p v-if="userid != '' && userid != null">当前登录账号{{ userid }} <el-button type="danger" @click="logout">退出</el-button></p>
        </el-col>
      </el-row>
  <p>本网站基于开源项目修改 项目地址：<a href="https://github.com/newlxj/stablediffusion-website-online">https://github.com/newlxj/stablediffusion-website-online</a></p>
    </div>
  </div>
</template>

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
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 设置高度以铺满整个屏幕 */
}

.content {
  text-align: center;
}

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
  
<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<template>
    <el-dialog class="dialogCss" v-model="dialogVisible" title="登录-Sign in" align-center :close-on-click-modal="false"
        :show-close="false" before-close="false">
        <el-tabs v-model="activeTab" class="demo-tabs">
            <el-tab-pane label="登录-Sign in" name="signin">
                <el-form :model="signinForm" ref="signinForm" :rules="rules" class="signin-form">
                    <el-form-item label="Email" prop="email">
                        <el-input v-model="signinForm.email"></el-input>
                    </el-form-item>
                    <el-form-item label="密码(Password)" prop="password">
                        <el-input type="password" v-model="signinForm.password"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="signin">登录</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="注册-Sign up" name="signup">
                <el-form :model="signupForm" ref="signupForm" :rules="rules"  class="signup-form">
                    <el-form-item label="注册Email" prop="email">
                        <el-input v-model="signupForm.email"></el-input>
                    </el-form-item>
                    <el-form-item label="注册密码(Password)" prop="password">
                        <el-input type="password" v-model="signupForm.password"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="signup">注册</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </el-dialog>
</template>

<style>
.demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.dialogCss {
    border-radius: 7px;
    width:90vw;
}
</style>
<script>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { SERVER_DOMAIN } from '../Config.vue'



export default {
    created() {
        
    },
    mounted() {
        this.$bus1.on('login_user', (data) => {
            if(data.loginshow){
                this.dialogVisible = true
            }else{
                this.dialogVisible = false
            }
        });

    },
    data() {
        // let activeTab = 'signin'
        // const dialogVisible = reactive(true)
        return {
            signinForm: reactive({
                email: '',
                password: ''
            }),
            signupForm: reactive({
                email: '',
                password: ''
            }),
            rules: {
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不能为空' },
                    { min: 8, message: '密码长度不能少于8位' },
                    { pattern: /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]{8,}$/, message: '密码必须包含字母和数字' }
                ]
            },
            dialogVisible: false,
            activeTab: 'signin',
        }
    }, methods: {
        handleClose() {
            this.activeTab = 'signin'
            this.signinForm.loginName = ''
            this.signinForm.password = ''
            this.signupForm.loginName = ''
            this.signupForm.email = ''
            this.signupForm.password = ''
            this.dialogVisible = false
            return false
        },
        signin() {
            const signinData = {
                email: this.signinForm.email,
                password: this.signinForm.password
            }

            this.$refs.signinForm.validate(valid => {
                if (!valid) {
                    // 校验不通过，给出相应的提示
                    console.log('校验不通过，请检查输入');
                    return
                } else {
                    fetch(SERVER_DOMAIN + '/api/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(signinData)
                    })

                        .then(response => response.json())
                        .then(data => {
                            if (data.code === 0) {
                                ElMessage({ message: '登录成功.', type: 'success', })
                                // localStorage.setItem('token', data.token)
                                this.$cookies.set("token", data.token,{expires: 1}); //方法到cookie方便校验
                                localStorage.setItem('userid', signinData.email)//放到Storage安全
                                this.dialogVisible = false
                                this.$bus1.emit("SelectPageRefresh", {});
                            } else {
                                ElMessage({ message: '登录失败.', type: 'error', })
                            }
                        })
                        .catch(error => {
                            // handle error
                        })
                }
            })



        },
        signup() {
            const signupData = {
                email: this.signupForm.email,
                password: this.signupForm.password
            }
            this.$refs.signupForm.validate(valid => {
                if (!valid) {
                    // 校验不通过，给出相应的提示
                    console.log('校验不通过，请检查输入');
                    return
                } else {
                    fetch(SERVER_DOMAIN + '/api/reg', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(signupData)
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.code === 1) {
                                // localStorage.setItem('token', data.token)
                                this.$cookies.set("token", data.token,{expires: 1}); //方法到cookie方便校验
                                localStorage.setItem('userid', signupData.email) //放到Storage安全
                                this.dialogVisible = false
                                this.$bus1.emit("SelectPageRefresh", {});
                                ElMessage({ message: '注册成功.', type: 'success' })
                            } else if (data.code === 2) {
                                ElMessage({ message: '邮箱' + this.signupForm.email + '已被注册，请检查.', type: 'warning' })
                            } else {
                                // handle signup failure
                                ElMessage({ message: '失败.', type: 'error' })
                            }
                        })
                        .catch(error => {
                            // handle error
                        })
                }
            })

        }
    }
}
</script>

  
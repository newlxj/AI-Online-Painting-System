// https://github.com/newlxj/stablediffusion-website-online for newlxj 
import { encryptJsonToStr, decryptStrToJson } from './crypto'
import { SERVER_DOMAIN } from '../Config.vue'
import Cookies from "js-cookie";
const myFetch = {
    install(Vue, options) {
        Vue.config.globalProperties.$myFetch = async function (urlpath, methodx, body, ContentType) {
            let header = {
                'Content-Type': 'text/plan; charset=utf-8'
            }
            let nbody = {}
            if (body == {} || body == null || body === undefined) {
                nbody = {}
            } else {
                nbody = encryptJsonToStr(body)
            }
            if (urlpath.indexOf("http") == -1) {
                urlpath = SERVER_DOMAIN + urlpath
            }
            const response = await fetch(urlpath, {
                method: methodx,
                headers: header,
                body: nbody
            }).then(response => {
                if (response.ok) {
                    return response.text()
                }else  if(response.status == 401) {
                    Cookies.remove("token")
                    localStorage.removeItem('userid')
                    this.$message.error('登录超时，请重新登录.');
                    this.$bus1.emit('login_user',{loginshow:true} );
                    // this.$router.push('/')
                }
            })
                .catch(error => {
                    this.$message.error('哟，出现了个未知错误.请刷新重新尝试或重新登录试试...');
                    // Cookies.remove("token")
                    // localStorage.removeItem('userid')
                    // this.$router.push('/')
                })
            // const response_1 = await response.text()
            return decryptStrToJson(response)
        }
    }
}

export default myFetch

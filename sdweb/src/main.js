// https://github.com/newlxj/stablediffusion-website-online for newlxj 
import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import router from './router/index.js'
import VueLazyload from 'vue-lazyload'
import mitt from 'mitt'
import myFetch from './util/myFetch'
import Cookies from "js-cookie";
const app = createApp(App)

const $bus = {}
const emitter = mitt()
$bus.on = emitter.on
$bus.emit = emitter.emit
$bus.off = emitter.off
app.config.globalProperties.$bus1 = $bus
app.config.globalProperties.$cookies = Cookies
app.config.globalProperties.$myFetch = myFetch

app.use(VueLazyload)

app.use(ElementPlus, {
    size: 'small',
    zIndex: 3000,
    locale: zhCn
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}


app.use(router)

app.use(myFetch)
app.mount('#app') 
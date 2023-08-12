// https://github.com/newlxj/stablediffusion-website-online for newlxj 
import { createRouter, createWebHistory } from "vue-router";  //导入路由
import Cookies from "js-cookie";
const routes = [
    {
        path: '/desktop', // 要路由到的url路径
        name: 'desktop',
        component: () => import('../page/Desktop.vue')
    },
    {
        path: '/viewer', // 要路由到的url路径
        name: 'viewer',
        component: () => import('../page/Mobile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/Go', // 要路由到的url路径
        name: 'Go',
        component: () => import('../page/Go.vue')
    },
    {
        path: '/r', // 要路由到的url路径
        name: 'r',
        component: () => import('../components/RandomTagDialog.vue')
    },
    {
        path: '/', // 要路由到的url路径
        name: 's',
        component: () => import('../page/Select.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/createModel', // 要路由到的url路径
        name: 'createModel',
        component: () => import('../page/CreatePage.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/login', // 要路由到的url路径
        name: 'login',
        component: () => import('../page/Login.vue'),
        meta: { requiresAuth: false }
    }
];


const router = createRouter({    // 定义一个路由器
    history: createWebHistory(),
    mode: "hash",
    routes
});

router.beforeEach((to, from, next) => {
    let token = Cookies.get("token") // localStorage.getItem('token')

    if (to.meta.requiresAuth && !token && token != "") { // 判断是否需要登录权限且未登录
        next('/') // 跳转到登录页
    } else {
        next() // 继续访问
    }
})

export default router;

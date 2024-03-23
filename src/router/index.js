import {createRouter, createWebHistory} from 'vue-router'

// 创建路由实例
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            component:() => import('@/views/layout/LayoutContainer.vue'),
            redirect: '/chat',
            children: [
                {
                    path: '/chat',
                    component: () => import('@/views/chat/ChatPage.vue')
                },
            ]
        },
        {
            path: '/login',
            component: () => import('@/views/login/LoginPage.vue')
        },
        {

        }
    ]
})

export default router
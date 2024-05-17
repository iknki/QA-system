import {createRouter, createWebHistory} from 'vue-router'
import {useUserStore} from "@/stores";


// 创建路由实例
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            component:() => import('@/views/layout/LayoutContainer.vue'),
            redirect: '/index',
            children: [
                {
                    path: '/index',
                    component: () => import('@/views/index/IndexPage.vue'),
                },
                {
                    path: '/chat',
                    components: {
                        default: () => import('@/views/chat/ChatPage.vue'),
                        aside: () => import('@/views/chat/ChatAside.vue'),
                    }
                },
                {
                    path: '/backendmanage',
                    components: {
                        default: () => import('@/views/backendmanage/BackendManagePage.vue'),
                        aside: () => import('@/views/backendmanage/BackendManageAside.vue'),
                    },
                    redirect: '/backendmanage/kbmanage',
                    children: [
                        {
                            path: '/backendmanage/kbmanage',
                            redirect: '/backendmanage/kbmanage/kblist',
                            children: [
                                {
                                    path: '/backendmanage/kbmanage/kblist',
                                    component: () => import('@/views/backendmanage/KBList.vue')
                                },
                                {
                                    path: '/backendmanage/kbmanage/knowledgelist',
                                    component: () => import('@/views/backendmanage/KnowledgeList.vue')
                                },
                            ]
                        },
                        {
                            path: '/backendmanage/model',
                            redirect: '/backendmanage/model/test',
                            children: [
                                {
                                    path: '/backendmanage/model/test',
                                    component: () => import('@/views/backendmanage/RecModelTest.vue')
                                },
                                {
                                    path: '/backendmanage/model/train',
                                    component: () => import('@/views/backendmanage/RecModelTrain.vue')
                                },
                            ]
                        },
                        {
                            path: '/backendmanage/usermanage',
                            component: () => import('@/views/backendmanage/UserManage.vue')
                        },
                        {
                            path: '/backendmanage/logs',
                            component: () => import('@/views/backendmanage/Logs.vue')
                        },
                        {
                            path: '/backendmanage/settings',
                            component: () => import('@/views/backendmanage/Settings.vue')
                        }
                    ]
                },
                {
                    path: '/user',
                    component: () => import('@/views/user/Personal.vue'),
                    redirect: '/user/info',
                    children: [
                        {
                            path: '/user/info',
                            component: () => import('@/views/user/Info.vue')
                        },
                        {
                            path: '/user/editPassword',
                            component: () => import('@/views/user/Editpassword.vue')
                        },
                        {
                            path: '/user/editAvatar',
                            component: () => import('@/views/user/EditAvatar.vue')
                        }
                    ]
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

// 登陆访问拦截
router.beforeEach((to, ) => {
    const usersStore = useUserStore()
    if (to.path !== '/login' && !usersStore.token) {
        return '/login'
    }
})

export default router
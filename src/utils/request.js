import axios from "axios"
import { useUserStore } from '@/stores'
import { ElMessage } from 'element-plus'
import router from '@/router'

//const baseURL = 'http://localhost:8000'
const baseURL = 'http://20.24.81.64:8000'
//const baseURL = 'https://8xrhkvwc-8000.asse.devtunnels.ms/'

const instance = axios.create({
    // 基地址，超时时间
    baseURL,
    timeout:30000
})

// 请求拦截器
instance.interceptors.request.use(
    (config) => {
        // 携带token
        const userStore = useUserStore()
        if (userStore.token) {
            config.headers.Authorization = userStore.token
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

//响应拦截器
instance.interceptors.response.use(
    (response) => {
        //return response.data;
        // 如果响应状态码为0，直接返回响应数据
        if (response.data.status === 0) {
            return response.data
        }
        // 处理业务失败（响应状态码为1），弹出提示
        ElMessage.error(response.data.message || '服务异常')
        return Promise.reject(response.data)
    },
    (error) => {
        // 错误默认情况
        ElMessage.error(error.response.data.content || '服务异常')
        return Promise.reject(error)

        //401错误（权限不足或token过期）=> 跳转登录页
        if (error.response.status === 401) {
            //清空token
            const userStore = useUserStore()
            userStore.logout()
            // 跳转登录页
            ElMessage.error("请先登录")
            router.push('/login')
        }
    }
)

export default instance
export { baseURL }
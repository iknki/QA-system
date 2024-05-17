import { createApp, ref, provide} from 'vue'
import App from './App.vue'
import pinia from '@/stores/index'
import router from './router'
import {MdPreview} from "md-editor-v3";
import "./assets/css/common.css";

const app = createApp(App)
const selected_sessionId = ref()
//export const baseURL= ref('http://10.8.0.6:8000')
export const baseURL = ref('http://20.24.81.64:8000')
//const baseURL = ref('http://localhost:8000')

app.use(pinia)
app.use(router)
app.component("MdPreview", MdPreview)

// 提供全局变量
app.provide('selected_sessionId', selected_sessionId)
app.provide('baseURL', baseURL)

app.mount('#app')

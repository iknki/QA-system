import { createApp, ref, provide} from 'vue'
import App from './App.vue'
import pinia from '@/stores/index'
import router from './router'
import {MdPreview} from "md-editor-v3";
import "./assets/css/common.css";

const app = createApp(App)
const selected_sessionId = ref()

app.use(pinia)
app.use(router)
app.component("MdPreview", MdPreview)

// 提供全局变量
app.provide('selected_sessionId', selected_sessionId)

app.mount('#app')

import { createPinia } from "pinia"
import persist from 'Pinia-plugin-persistedstate'

const pinia = createPinia()

pinia.use(persist)

export default pinia

// 暴露stores接口
export * from './modules/user'
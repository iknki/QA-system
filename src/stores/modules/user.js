import {defineStore} from "pinia";
import {ref} from "vue";

export const  useUserStore = defineStore('User',() =>{
    const token =ref()
    const sessionid = ref()
    const setToken = (newToken) => {
        token.value = newToken
    }
    const removeToken = () => {
        token.value = ''
    }
    const setSessionid = (newSessionid) => {
        sessionid.value = newSessionid
    }
    const removeSessionid = () => {
        sessionid.value = ''
    }
    return{
        token,
        sessionid,
        setToken,
        removeToken,
        setSessionid,
        removeSessionid
    }
},
    {
    persist: true
})
import {defineStore} from "pinia";
import {ref} from "vue";

export const  useUserStore = defineStore('User',() =>{
    const token =ref()
    const sessionid = ref()
    const username = ref()
    const password = ref()
    const checked = ref(false)
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
    const setRemember = ({Username, Password}) => {
        console.log(Username, Password)
        username.value = Username
        password.value = Password
        checked.value = true
    }
    const removeRemember = () => {
        username.value = ''
        password.value = ''
        checked.value = false
    }
    const logout = () => {
        token.value = ''
        sessionid.value = ''
    }
    return{
        token,
        sessionid,
        username,
        password,
        checked,
        setToken,
        removeToken,
        setSessionid,
        removeSessionid,
        setRemember,
        removeRemember,
        logout
    }
},
    {
    persist: true
})
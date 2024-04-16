import {defineStore} from "pinia";
import {ref} from "vue";

export const chatBufferStore = defineStore('ChatBuffer', () => {
    const sessions = ref([])
    const messages = ref([])

    return {
        sessions,
        messages
    }
})
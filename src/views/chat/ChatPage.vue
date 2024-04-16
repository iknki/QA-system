<script setup>
import {ref, watch, onMounted, inject, onBeforeUnmount} from 'vue';
import MessageRow from "@/components/MessageRow.vue";
import {chatGetAnswerService, chatGetMessagesService} from "@/api/chat";
import {chatBufferStore} from "@/stores/index.js";


const messages = ref([])
const selected_sessionId = inject('selected_sessionId')
const bufferStore = chatBufferStore()
const table_loading = ref(false);


const inputmessage = ref('')
const SendMessage = (event) => {
  console.log('inputmessage')
  if(!event.shiftKey) {
    if (inputmessage.value==='\n') {
      ElMessage({
        message: '请输入内容',
        type: 'warning',
        offset: 100
      })
      inputmessage.value = ''
    }
    else {
      messages.value.push({role: 'user', content: inputmessage.value})
      GetAnswer(inputmessage)
      inputmessage.value = ''
    }
  }
}

const SendMessageButton = () => {
  console.log('inputmessage')
    if (!inputmessage.value) {
      ElMessage({
        message: '请输入内容',
        type: 'warning',
        offset: 100
      })
    }
    else {
      messages.value.push({role: 'user', content: inputmessage.value})
      GetAnswer(inputmessage)
      inputmessage.value = ''
    }
}

const GetAnswer = async (question) => {
  console.log('GetAnswer')
  messages.value.push({role: 'robot', content: ''})
  const lastMessageIndex = messages.value.length - 1;
  // 调用 chatGetAnswerService 获取回答
  try {
    console.log('chatGetAnswerService is running')
    const response = await chatGetAnswerService({
          sessionId:selected_sessionId.value,
          question:question.value
        })
    messages.value[lastMessageIndex].content = response.messages[0].content
    console.log('Success fetching chat answer')
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取回答失败，请重试！');
    console.error('Error fetching chat messages:', error);
  }
}

// 初始化，获取历史记录
const Init = async (sessionid) => {
  try {
    table_loading.value = true;
    console.log('watch selected_sessionId')
    console.log('sessionId:', sessionid.value)
    messages.value = []
    // 调用 chatGetMessagesService 获取历史对话信息
    console.log('chatGetMessagesService is running')
    const response = await chatGetMessagesService({sessionId:sessionid});
    messages.value = response.messages;
    // 如果成功获取到历史对话信息，则更新 messages 变量
    console.log(messages)
    console.log('Success fetching chat messages:')
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取历史对话信息失败，请重试！');
    console.error('Error fetching chat messages:', error);
    table_loading.value = false;
  }
}


watch(selected_sessionId, async (newvalue, oldValue) => {
  Init(newvalue)
})

onMounted(() => {
  if(bufferStore.messages.length !== 0){
    console.log('读取缓存')
    messages.value = bufferStore.messages.value
    console.log('读取缓存成功')
  }
  else {
    if (selected_sessionId.value !== undefined) {
      Init(selected_sessionId.value)
    }
  }
})

onBeforeUnmount(() => {
  console.log('缓存中')
  bufferStore.messages.value = messages.value
  console.log('缓存成功')
})



</script>

<template>
  <el-main v-loading="table_loading">
    <div class="message-panel">
      <MessageRow v-for="message in messages" :role="message.role" :content="message.content"></MessageRow>
    </div>
  </el-main>
  <el-footer height="140px" style="margin-top: 20px">
    <el-form autocomplete="on" >
      <el-form-item>
        <div class="input_container">
          <el-input
              v-model="inputmessage"
              :autosize="{ minRows: 3, maxRows: 6 }"
              type="textarea"
              placeholder="在此输入你想要了解的内容"
              @keyup.enter.native="SendMessage"
              resize="none"
          />
          <el-button type="primary" @click="SendMessageButton">发送</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-footer>

</template>

<style lang="scss" scoped>
.message-panel {
  margin: 0 auto;
  margin-top: 60px;
  width: 800px;
  overflow: hidden;
}

.input_container {
  display: flex;
  margin: 0 auto;
  width: 800px;
  border: #747bff;
  height: 100%;

}

.input_container >>> .el-textarea__inner {
  border: 0 !important;
  resize: none; /* 这个是去掉 textarea 下面拉伸的那个标志 */
}
</style>
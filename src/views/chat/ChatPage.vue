<script setup>
import {ref, watch, onMounted, inject, onBeforeUnmount} from 'vue';
import MessageRow from "@/components/MessageRow.vue";
import {chatGetAnswerService, chatGetMessagesService, chatGetRecommendQuestionsService} from "@/api/chat";
import {chatBufferStore} from "@/stores/index.js";
import {useUserStore} from "@/stores/index.js";

const userStore = useUserStore()
const messages = ref([])
const selected_sessionId = inject('selected_sessionId')
const bufferStore = chatBufferStore()
const table_loading = ref(false);
const questions = ref([])

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

// 刷新推荐问题序列
const refresh = async () => {
  console.log('refresh')
  const response = await chatGetRecommendQuestionsService({question:null, userId:userStore.token.id, flag:true});
  questions.value = response.questions
}

const GetAnswer = async (question) => {
  console.log('GetAnswer')
  messages.value.push({role: 'robot', content: ''})
  const lastMessageIndex = messages.value.length - 1;
  // 调用 chatGetAnswerService 获取回答
  try {
    console.log('chatGetAnswerService is running')
    // 同时执行chatGetAnswerService和chatGetRecommendQuestionsService
    const [messagesResponse, questionsResponse] = await Promise.all([
      chatGetAnswerService({
        sessionId:selected_sessionId.value,
        question:question.value,
        userId: userStore.token.id
      }),
      chatGetRecommendQuestionsService({ question: question.value, userId: userStore.token.id })
    ]);

    // 将获取到的消息和推荐问题分别存储到messages.value和questions.value中
    messages.value[lastMessageIndex].content = messagesResponse.messages[0].content
    questions.value = questionsResponse.questions;
    console.log('Success fetching chat answer')
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取回答失败，请重试！');
    console.error('Error fetching chat messages:', error);
  }
}

// 从推荐问题处选择问题
const onSelectQuestion = (question) => {
  inputmessage.value = question
  SendMessageButton()
}

// 初始化，获取历史记录
const Init = async (sessionid) => {
  try {
    questions.value = []
    table_loading.value = true;
    console.log('watch selected_sessionId')
    console.log('sessionId:', sessionid.value)
    messages.value = []
    // 调用 chatGetMessagesService 获取历史对话信息
    console.log('chatGetMessagesService is running')
    // 同时执行chatGetMessagesService和chatGetRecommendQuestionsService
    const [messagesResponse, questionsResponse] = await Promise.all([
      chatGetMessagesService({ sessionId: sessionid, userId: userStore.token.id }),
      chatGetRecommendQuestionsService({ question: null, userId: userStore.token.id })
    ]);

    // 将获取到的消息和推荐问题分别存储到messages.value和questions.value中
    messages.value = messagesResponse.messages;
    questions.value = questionsResponse.questions;
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
    <div style="display: flex; margin: 0 auto; width: 60vw; margin-bottom: 10px">
      <el-button style="background-color: transparent; border: none; padding: 0" @click="refresh">
        <el-tooltip
            placement="top"
            content="刷新"
            trigger="hover"
            :width="10"
        >
          <i-ep-refresh style="color: #5274F3; font-size: 16px"/>
        </el-tooltip>
      </el-button>
      <span style="margin-top: 4px;width:90px"> 推荐问:</span>
      <el-card class="recommend_question" body-style="padding:0;margin:3px 8px 3px 8px; font-size:12px" v-for="question in questions" shadow="hover" @click="onSelectQuestion(question)"> {{ question }} </el-card>
    </div>
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
  width: 60vw;
  overflow: hidden;
}

.input_container {
  display: flex;
  margin: 0 auto;
  width: 60vw;
  border: #747bff;
  height: 100%;

}

.input_container >>> .el-textarea__inner {
  border: 0 !important;
  resize: none; /* 这个是去掉 textarea 下面拉伸的那个标志 */
}

.recommend_question {
  margin-left:5px;
  margin-right:5px;
}
.recommend_question:hover {
  cursor: pointer;
}
</style>
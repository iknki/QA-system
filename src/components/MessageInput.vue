<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['input'])

const inputmessage = ref('')



const SendMessage = async (event) => {
  console.log(inputmessage)
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
      console.log('MessageInput')
      setTimeout(() => {
        emit('input', inputmessage.value);
        inputmessage.value = '';
      }, 0)
    }
  }
}
const SendMessageButton = () => {
    if (!inputmessage.value) {
      ElMessage({
        message: '请输入内容',
        type: 'warning',
        offset: 100
      })
    } else {
      console.log('MessageInput')
      emit('input', String(inputmessage.value))
      inputmessage.value = ''
    }

}

</script>

<template>
  <el-footer height="140px" style="margin-top: 20px">
    <el-form autocomplete="on" class="input_container">
      <el-form-item>
        <div>
          <el-input
              v-model="inputmessage"
              :autosize="{ minRows: 3, maxRows: 6 }"
              type="textarea"
              placeholder="在此输入你想要了解的内容"
              @keyup.enter.native="SendMessage"
          />
          <el-button type="primary" @click="SendMessageButton">发送</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-footer>
</template>

<style scoped>
.input_container {
  margin: 0 auto;
  width: 800px;
  border: #747bff;
  height: 100%;
  div {
    display: flex;
    width: 100%;
  }
}

.input_container >>> .el-textarea__inner {
  border: 0 !important;
  resize: none; /* 这个是去掉 textarea 下面拉伸的那个标志 */
}


</style>
<script setup>
import {ref, defineExpose} from 'vue'
import {knowledgebaseCreateKBService, knowledgebaseEditKBService} from '@/api/knowledgebase.js'
import {useUserStore} from '@/stores/index.js'
import {ElMessage} from "element-plus";

const DialogVisible = ref(false)
const userStore = useUserStore()
const index = ref()
const isloading = ref(false)

const formRef = ref()
const defaultformModel = ref({
  kbid: null,
  kbname: '',
  info: ''
})
const formModel = ref({})

const rules = {
  kbname: [
    {required: true, message: '请输入知识库名称', trigger: 'blur'},
    {
      pattern: /^\S{1,10}$/,
      message: '知识库名称长度不能超过10个字符',
      trigger: 'blur'
    }
  ]
}

const emit = defineEmits(['success'])
const onSubmit = async () => {
  isloading.value = true
  const isEdit = formModel.value.kbid
  console.log('onSubmit')
  await formRef.value.validate()
  if(isEdit) {
    // 编辑知识库
    const response = await knowledgebaseEditKBService({
      kbId: formModel.value.kbid,
      kbname: formModel.value.kbname,
      info: formModel.value.info
    })
    ElMessage.success(response.message)
    isloading.value = false
  } else {
    // 新建知识库
    const response = await knowledgebaseCreateKBService({
      userId: userStore.token.id,
      kbname: formModel.value.kbname,
      info: formModel.value.info
    })
    ElMessage.success(response.message)
    isloading.value = false
  }
  DialogVisible.value = false
  emit('success')
}

const openDialog = (row, index) => {
  console.log('openDialog')
  DialogVisible.value = true
  if(row){
    formModel.value = {...row}
  }
  else {
    formModel.value = {...defaultformModel.value}
  }
  index.value = index
}

defineExpose({
  openDialog

})

</script>

<template>
  <el-dialog v-model="DialogVisible" :title="formModel.kbid ? '编辑知识库': '新建知识库'" width="30%" center v-loading="isloading">
    <el-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-width="100px"
        style="padding-right: 30px">
      <el-form-item label="知识库名称" prop="kbname" style="margin-bottom: 20px">
        <el-input v-model="formModel.kbname" placeholder="请输入知识库名称">
        </el-input>
      </el-form-item>
      <el-form-item label="知识库名称" prop="info" style="margin-bottom: 20px">
        <el-input v-model="formModel.info" placeholder="请输入知识库信息">
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="DialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
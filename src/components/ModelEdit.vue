<script setup>
import {ref, defineExpose} from 'vue'
import {useUserStore} from '@/stores/index.js'
import {ElMessage} from "element-plus";
import {modelEditModelService} from "@/api/model.js";

const DialogVisible = ref(false)
const userStore = useUserStore()
const index = ref()
const isloading = ref(false)

const formRef = ref()
const formModel = ref({})

const rules = {
  modelname: [
    {required: true, message: '请模型名称', trigger: 'blur'},
    {
      pattern: /^\S{1,10}$/,
      message: '模型名称长度不能超过10个字符',
      trigger: 'blur'
    }
  ]
}

const emit = defineEmits(['success'])
const onSubmit = async () => {
  isloading.value = true
  console.log('onSubmit')
  await formRef.value.validate()
  // 编辑模型
  const response = await modelEditModelService({
    model: formModel.value,
    userid: userStore.token.id
  })
  ElMessage.success(response.message)
  isloading.value = false
  DialogVisible.value = false
  emit('success')
}

const openDialog = (row) => {
  console.log('openDialog')
  DialogVisible.value = true
  formModel.value = {...row}
  console.log('formModel', formModel)
}

defineExpose({
  openDialog

})

</script>

<template>
  <el-dialog v-model="DialogVisible" title="编辑模型" width="30%" center v-loading="isloading">
    <el-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-width="100px"
        style="padding-right: 30px">
      <el-form-item label="知识库名称" prop="modelname" style="margin-bottom: 20px">
        <el-input v-model="formModel.modelname" placeholder="请输入知识库名称">
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
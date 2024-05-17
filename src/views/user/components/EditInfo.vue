<script setup>
import {ref, defineExpose} from 'vue'
import {useUserStore} from '@/stores/index.js'
import {ElMessage} from "element-plus";
import {userEditUserInfoService} from "@/api/user.js";

const DialogVisible = ref(false)
const userStore = useUserStore()
const index = ref()
const isloading = ref(false)

const formRef = ref()
const formModel = ref({
  username: '',
  nickname: '',
  age: '',
  sex: '',
  email: '',
  phone: '',
  area: '',
  job: ''
})

const rules = {
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'}
  ],
}

const emit = defineEmits(['success'])
const onSubmit = async () => {
  isloading.value = true
  console.log('onSubmit')
  await formRef.value.validate()

  const response = await userEditUserInfoService({userInfo: formModel.value, userid: userStore.token.id})
  ElMessage.success(response.message)
  isloading.value = false
  DialogVisible.value = false
  emit('success')
}

const openDialog = (data) => {
  console.log('openDialog')
  DialogVisible.value = true
  formModel.value = {...data}
  console.log('formModel', formModel)
}

defineExpose({
  openDialog

})

</script>

<template>
  <el-dialog v-model="DialogVisible" title="编辑个人信息" width="30%" center
             v-loading="isloading">
    <el-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-width="auto"
        :label-position="'right'"
        style="padding-right: 30px; padding-left: 30px"
    >
      <el-form-item label="用户名" prop="username">
        <el-input size="large" v-model="formModel.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input size="large" v-model="formModel.nickname" placeholder="请输入昵称"></el-input>
      </el-form-item>
      <el-form-item label="年龄" prop="age">
        <el-input size="large" v-model="formModel.age" placeholder="请输入年龄"></el-input>
      </el-form-item>
      <el-form-item label="性别" prop="sex">
        <el-input size="large" v-model="formModel.sex" placeholder="请输入性别"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input size="large" v-model="formModel.email" placeholder="请输入邮箱"></el-input>
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input size="large" v-model="formModel.phone" placeholder="请输入手机号"></el-input>
      </el-form-item>
      <el-form-item label="地区" prop="area">
        <el-input size="large" v-model="formModel.area" placeholder="请输入地区"></el-input>
      </el-form-item>
      <el-form-item label="职业" prop="job">
        <el-input size="large" v-model="formModel.job" placeholder="请输入职业"></el-input>
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
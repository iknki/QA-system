<script setup>

import {ref} from 'vue'
import {useUserStore} from '@/stores/index.js'
import {userEditPasswordService} from '@/api/user.js'

const userStore = useUserStore()

const formRef = ref()
const formModel = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const checkRePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次确认密码'))
  } else if (value !== formModel.value.newPassword) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}
const rules = {
  oldPassword: [
    {required: true, message: '请输入原密码', trigger: 'blur'}
  ],
  newPassword: [
    {required: true, message: '请输入新密码', trigger: 'blur'}
  ],
  confirmPassword: [
    {required: true, message: '请再次输入新密码', trigger: 'blur'},
    {validator: checkRePassword, trigger: 'blur'},
  ]
}

const onSubmit = async () => {
  try {
    await formRef.value.validate()
    console.log('onSubmit')
    const response = await userEditPasswordService({
      oldpassword: formModel.value.oldPassword,
      newpassword: formModel.value.newPassword,
      username: userStore.token.username
    })
    ElMessage.success(response.message)
  } catch (error) {
    console.log('error', error)
  }
}

</script>

<template>
  <el-card style="height: 80vh">
    <el-row>
      <el-col :span="8" :offset="6">
        <el-form
            ref="formRef"
            label-width="auto"
            :model="formModel"
            :rules="rules"
            :label-position="'right'"
            style="margin-top: 20vh"
        >
          <el-form-item label="原密码" prop="oldPassword">
            <el-input size="large" show-password v-model="formModel.oldPassword"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input size="large" show-password v-model="formModel.newPassword"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input size="large" show-password v-model="formModel.confirmPassword"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit" style="margin-left: 30%">提交</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </el-card>
</template>

<style scoped>

</style>
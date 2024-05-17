<script setup>
import {ref, defineExpose} from 'vue'
import {useUserStore} from '@/stores/index.js'
import {ElMessage} from "element-plus";
import {userCreateUserService, userEditUserService} from "@/api/user.js";

const DialogVisible = ref(false)
const userStore = useUserStore()
const index = ref()
const isloading = ref(false)

const formRef = ref()
const defaultformModel = ref({
  userid: null,
  username: '',
  password: '',
  role: ''
})
const formModel = ref({})

const rules = {
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
  ],
  role: [
    {
      required: true,
      validator: (rule, value, callback) => {
        if (value === null) {
          callback(new Error('请选择用户角色'));
        } else {
          callback();
        }
      },
      trigger: 'submit'
    }
  ],
}

const emit = defineEmits(['success'])
const onSubmit = async () => {
  isloading.value = true
  const isEdit = formModel.value.userid
  console.log('onSubmit')
  await formRef.value.validate()
  if(isEdit) {
    // 编辑用户
    const response = await userEditUserService({
      username: formModel.value.username,
      password: formModel.value.password,
      role: formModel.value.role,
      userid: formModel.value.userid
    })
    ElMessage.success(response.message)
    isloading.value = false
  } else {
    // 新建用户
    const response = await userCreateUserService({
      username: formModel.value.username,
      password: formModel.value.password,
      role: formModel.value.role
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
  <el-dialog v-model="DialogVisible" :title="formModel.userid ? '编辑用户': '新增用户'" width="30%" center v-loading="isloading">
    <el-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-width="100px"
        style="padding-right: 30px">
      <el-form-item label="用户名" prop="username" style="margin-bottom: 20px">
        <el-input v-model="formModel.username" placeholder="请输入用户名">
        </el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password" style="margin-bottom: 20px">
        <el-input v-model="formModel.password" placeholder="请输入用户密码">
        </el-input>
      </el-form-item>
      <el-form-item label="用户角色" prop="role" style="margin-bottom: 20px">
        <el-select v-model="formModel.role" placeholder="请选择用户角色">
          <el-option label="管理员" value="admin"></el-option>
          <el-option label="普通用户" value="user"></el-option>
        </el-select>
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
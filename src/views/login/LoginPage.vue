<script setup>

import {ref, watch, onMounted} from "vue";
import {userEditPasswordService, userLoginService, userRegisterService} from "@/api/user";
import {useUserStore} from "@/stores/index.js";
import {useRouter} from "vue-router";
import backround from '@/assets/backround.jpg'


const isRegister = ref(false);
const isEdit = ref(false);
const form = ref(null)
const userStore = useUserStore()
const router = useRouter()

const formModel = ref({
  username: '',
  password: '',
  rePassword: '',
  newpassword: ''
});





watch(isRegister,() => {
  formModel.value = {
    username: '',
    password: '',
    rePassword: ''
  }
})
watch(isEdit,() => {
  formModel.value = {
    username: '',
    password: '',
    rePassword: '',
    newpassword: '',
  }
})


const checkRePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次确认密码'))
  } else if (value !== formModel.value.Password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}
const rules = {
  Username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
    {min: 5, max: 16, message: '长度为5-16位', trigger: 'blur'},
  ],
  Password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 5, max: 16, message: '长度为5-16位', trigger: 'blur'},
  ],
  rePassword: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {validator: checkRePassword, trigger: 'blur'},
  ]
};

const register = async () => {
  await form.value.validate(async (valid) => {
    if (valid) {
      console.log('注册处理中')
      const response = await userRegisterService(formModel.value);
      console.log(response)
      ElMessage.success(response ? response.message : '注册成功')
      isRegister.value = false
      console.log('注册处理完成')
    }
  })
}
const login = async () => {
  await form.value.validate(async (valid) => {
    if (valid) {
      console.log('登陆处理中')
      if(userStore.checked){
        console.log('记住密码')
        userStore.setRemember(formModel.value)
      }
      const response = await userLoginService(formModel.value);
      console.log(response)
      userStore.setToken(response.token)
      ElMessage.success(response ? response.message : '登陆成功')
      console.log('登陆处理完成')
      router.push({path: '/'})
    }
  })
}

const update = async () => {
  try {
    await form.value.validate()
    console.log('更新密码')
    const response = await userEditPasswordService({
      oldpassword: formModel.value.password,
      newpassword: formModel.value.newpassword,
      username: formModel.value.username
    })
    ElMessage.success(response.message)
    isEdit.value = false
  } catch (error) {
    console.log('error', error)
  }
}

onMounted(() => {
  if(userStore.checked){
    console.log(userStore.username)
    formModel.value = {
      username: userStore.username,
      password: userStore.password,
      rePassword: ''
    }
  }
})

</script>

<template>
  <el-row class="login-page">
    <el-col :span="8">
      <el-card v-if="!isEdit">
        <!--   注册表单   -->
        <el-form ref="form" size="large" autocomplete="on" v-if="isRegister" :model="formModel" :rules="rules">
          <el-form-item>
            <h1 style="margin: 0 auto">注册</h1>
          </el-form-item>
          <el-form-item prop="Username">
            <el-input v-model="formModel.Username" placeholder="请输入用户名">
              <template #prefix>
                <i-ep-User style="float:left"></i-ep-User>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="Password">
            <el-input v-model="formModel.Password" type="password" placeholder="请输入密码">
              <template #prefix>
                <i-ep-Lock style="float:left"></i-ep-Lock>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="rePassword">
            <el-input v-model="formModel.rePassword" type="password" placeholder="请输入再次密码">
              <template #prefix>
                <i-ep-Lock style="float:left"></i-ep-Lock>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" round auto-insert-space @click="register">注册</el-button>
          </el-form-item>
          <el-form-item class="flex">
            <el-link type="info" :underline="false" @click="isRegister = false">
              ← 去登陆
            </el-link>
          </el-form-item>
        </el-form>
        <!--   登陆表单   -->
        <el-form ref="form" size="large" autocomplete="on" v-else :model="formModel" :rules="rules">
          <el-form-item>
            <h1 style="margin: 0 auto">登陆</h1>
          </el-form-item>
          <el-form-item prop="Username">
            <el-input v-model="formModel.Username" placeholder="请输入用户名">
              <template #prefix>
                <i-ep-User style="float:left"></i-ep-User>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="Password">
            <el-input v-model="formModel.Password" type="password" placeholder="请输入密码">
              <template #prefix>
                <i-ep-Lock style="float:left"></i-ep-Lock>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <div class="flex">
              <el-checkbox v-model="userStore.checked">记住我</el-checkbox>
              <el-link type="primary" :underline="false" @click="isEdit = true">修改密码</el-link>
            </div>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" round auto-insert-space @click="login">登录</el-button>
          </el-form-item>
          <el-form-item>
            <el-link type="info" :underline="false" @click="isRegister = true">
              去注册 →
            </el-link>
          </el-form-item>
        </el-form>
      </el-card>
      <el-card v-else>
        <!--   修改密码表单   -->
        <el-form ref="form" size="large" autocomplete="on" v-if="isEdit" :model="formModel" :rules="rules">
          <el-form-item>
            <h1 style="margin: 0 auto">修改密码</h1>
          </el-form-item>
          <el-form-item prop="username">
          <el-input v-model="formModel.username" placeholder="请输入用户名">
            <template #prefix>
              <i-ep-User style="float:left"></i-ep-User>
            </template>
          </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="formModel.password" type="password" placeholder="请输入密码">
              <template #prefix>
                <i-ep-Lock style="float:left"></i-ep-Lock>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="newpassword">
            <el-input v-model="formModel.newpassword" type="password" placeholder="请输入新密码">
              <template #prefix>
                <i-ep-Lock style="float:left"></i-ep-Lock>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" round auto-insert-space @click="update">更新密码</el-button>
          </el-form-item>
          <el-form-item>
            <el-link type="info" :underline="false" @click="isEdit = false">
              返回登陆 →
            </el-link>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>

</template>

<style lang="scss" scoped>
.login-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url("@/assets/backround.jpg") no-repeat center center;
  background-size: cover;
}

.el-button {
  margin: 0 auto;
}

.flex {
  width: 100%;
  display: flex;
  justify-content: space-between;
}


</style>
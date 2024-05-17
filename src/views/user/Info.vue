<script setup>
import { ref, onMounted } from 'vue'
import {userGetUserInfoService} from "@/api/user.js";
import {useUserStore} from "@/stores/index.js";
import {ElMessage} from "element-plus";
import EditInfo from "@/views/user/components/EditInfo.vue";

const userStore = useUserStore()

const user = ref({
  username: '',
  nickname: '',
  age: '',
  sex: '',
  email: '',
  phone: '',
  area: '',
  job: ''
})
const dialog = ref();


const onEditInfo = () => {
  console.log('onEditInfo')
  dialog.value.openDialog(user.value)
}


const getUserInfo = async () => {
  try {
    const response = await userGetUserInfoService({userid: userStore.token.id})
    user.value = response.userinfo
  } catch (error) {
    ElMessage.error('获取用户信息失败')
    console.log(error)
  }
}

const onSuccess = () => {
  getUserInfo()
}

onMounted(() => {
  getUserInfo()
})

</script>

<template>
  <el-card class="container">
    <el-descriptions class="margin-top" title="简介" :column="2" border>
      <template #extra>
        <el-button type="primary" @click="onEditInfo">编辑资料</el-button>
      </template>
      <el-descriptions-item label="用户名" label-align="right" align="center">
        {{ user.username }}
      </el-descriptions-item>
      <el-descriptions-item label="昵称" label-align="right" align="center">
        {{ user.nickname }}
      </el-descriptions-item>
      <el-descriptions-item label="年龄" label-align="right" align="center">
        {{ user.age }}
      </el-descriptions-item>
      <el-descriptions-item label="性别" label-align="right" align="center">
        {{ user.sex }}
      </el-descriptions-item>
      <el-descriptions-item label="邮箱" label-align="right" align="center">
        {{ user.email }}
      </el-descriptions-item>
      <el-descriptions-item label="手机号" label-align="right" align="center">
        {{ user.phone }}
      </el-descriptions-item>
      <el-descriptions-item label="地区" label-align="right" align="center">
        {{ user.area }}
      </el-descriptions-item>
      <el-descriptions-item label="职业" label-align="right" align="center">
        {{ user.job }}
      </el-descriptions-item>
      <el-descriptions-item label="注册时间" label-align="right" align="center">
        {{ user.timestamp }}
      </el-descriptions-item>
    </el-descriptions>
  </el-card>
  <EditInfo ref="dialog" @success="onSuccess"/>
</template>

<style scoped>

.container {
  min-height: 80vh;
}

</style>
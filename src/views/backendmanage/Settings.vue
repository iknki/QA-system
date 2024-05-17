<script setup>

import PageContainer from "@/components/PageContainer.vue";
import { baseURL } from "@/main.js";
import {ElMessage} from "element-plus";
import {settingGetSettingsService, settingEditSettingsService} from "@/api/setting.js";
import {ref, watch, onMounted} from 'vue'
import {useUserStore} from "@/stores/index.js";
import ModelSelect from "@/components/ModelSelect.vue";

const test = ref(false)
const edit = ref(false)
const formRef = ref()
const loading = ref(false)
const userStore = useUserStore()


const defaultSettings = ref({})
const settings = ref({
  llm: {
    appid: '',
    api_secret: '',
    api_key: '',
  },
  recommendModel: {
    model_id: null
  },
  mysql: {
    database: '',
    port: '',
    user: '',
    password: ''
  },
  es: {
    port: '',
    user: '',
    password: ''
  },
  test: ''
})


const rules = {
  'llm.appid': [
    {required: true, message: '请输入APPID', trigger: 'blur'}
  ],
  'llm.api_secret': [
    {required: true, message: '请输入APISecret', trigger: 'blur'}
  ],
  'llm.api_key': [
    {required: true, message: '请输入APIKey', trigger: 'blur'}
  ],
  'recommendModel.model_id': [
    {
      required: true,
      validator: (rule, value, callback) => {
        if (value === null) {
          callback(new Error('请选择要测试的模型'));
        } else {
          callback();
        }
      },
      trigger: 'submit'
    }
  ],
  'mysql.database': [
    {required: true, message: '请输入数据库名', trigger: 'blur'}
  ],
  'mysql.port': [
    {required: true, message: '请输入数据库端口', trigger: 'blur'}
  ],
  'mysql.user': [
    {required: true, message: '请输入数据库用户名', trigger: 'blur'}
  ],
  'mysql.password': [
    {required: true, message: '请输入数据库密码', trigger: 'blur'}
  ],
  'es.port': [
    {required: true, message: '请输入ES端口', trigger: 'blur'}
  ],
  'es.user': [
    {required: true, message: '请输入ES用户名', trigger: 'blur'}
  ],
  'es.password': [
    {required: true, message: '请输入ES密码', trigger: 'blur'}
  ],
  test: [
    {required: true, message: '请输入测试输入', trigger: 'blur'}
  ]
}

const getSettings = async () => {
  try {
    console.log('getSettings')
    loading.value = true
    const response = await settingGetSettingsService()
    settings.value = response.settings
    defaultSettings.value = response.settings
    console.log('settings', settings.value)
    loading.value = false
  } catch (error) {
    ElMessage.error('获取系统设置失败')
    console.log('error', error)
    loading.value = false
  }
}

const onReset = () => {
  settings.value = defaultSettings.value
  edit.value = false
}

const onSubmit = async () => {
  try {
    await formRef.value.validate()
    const response = await settingEditSettingsService({
      settings: settings.value
    })
    ElMessage.success(response.message)
  } catch (error) {
    ElMessage.error('保存设置失败')
    console.log('error', error)
  }
}


watch(() => settings.value, (newVal) => {
  edit.value = true
}, {deep: true})

onMounted(async () => {
  await getSettings()
  edit.value = false
})

</script>

<template>
  <el-main>
    <page-container title="系统设置">
      <el-row>
        <el-col :span="10" :offset="6">
            <el-form
                ref="formRef"
                :model="settings"
                :rules="rules"
                style="width: 100%"
                label-width="auto"
                :label-position="'right'"
                v-loading="loading"
            >
              <h3>服务设置</h3>
              <el-form-item label="后端服务URL" size="large">
                <el-input v-model="baseURL" placeholder="请输入后端系统服务URL"></el-input>
              </el-form-item>
              <h3>大语言模型API设置</h3>
              <el-form-item label="APPID" size="large" prop="llm.appid">
                <el-input v-model="settings.llm.appid" placeholder="请输入APPID"></el-input>
              </el-form-item>
              <el-form-item label="APISecret" size="large" prop="llm.api_secret">
                <el-input v-model="settings.llm.api_secret" placeholder="请输入APISecret"></el-input>
              </el-form-item>
              <el-form-item label="APIKey" size="large" prop="llm.api_key">
                <el-input v-model="settings.llm.api_key" placeholder="请输入APIKey"></el-input>
              </el-form-item>
              <h3>问题推荐模型设置</h3>
              <el-form-item label="选择问题推荐模型" size="large" prop="recommendModel.model_id">
                <ModelSelect v-model="settings.recommendModel.model_id"></ModelSelect>
              </el-form-item>
              <h3>Mysql数据库设置</h3>
              <el-form-item label="数据库名" size="large" prop="mysql.database">
                <el-input v-model="settings.mysql.database" placeholder="请输入数据库名"></el-input>
              </el-form-item>
              <el-form-item label="数据库端口" size="large" prop="mysql.port">
                <el-input v-model="settings.mysql.port" placeholder="请输入数据库端口"></el-input>
              </el-form-item>
              <el-form-item label="数据库用户名" size="large" prop="mysql.user">
                <el-input v-model="settings.mysql.user" placeholder="请输入数据库用户名"></el-input>
              </el-form-item>
              <el-form-item label="数据库密码" size="large" prop="mysql.password">
                <el-input v-model="settings.mysql.password" placeholder="请输入数据库密码"></el-input>
              </el-form-item>
              <h3>ElasticSearch知识库设置</h3>
              <el-form-item label="ES端口" size="large" prop="es.port">
                <el-input v-model="settings.es.port" placeholder="请输入ES端口"></el-input>
              </el-form-item>
              <el-form-item label="ES用户名" size="large" prop="es.user">
                <el-input v-model="settings.es.user" placeholder="请输入ES用户名"></el-input>
              </el-form-item>
              <el-form-item label="ES密码" size="large" prop="es.password">
                <el-input v-model="settings.es.password" placeholder="请输入ES密码"></el-input>
              </el-form-item>
              <h3 v-if="test">测试</h3>
              <el-form-item label="测试输入" size="large" prop="test" v-if="test">
                <el-input v-model="settings.test" placeholder="测试输入"></el-input>
              </el-form-item>
              <el-form-item>
                <div style="display: flex;margin-left: 30%">
                  <el-button type="primary" @click="onSubmit" :disabled="!edit">保存修改</el-button>
                  <el-button @click="onReset">重置修改</el-button>
                </div>

              </el-form-item>
            </el-form>
        </el-col>
      </el-row>
    </page-container>
  </el-main>

</template>

<style scoped>

</style>
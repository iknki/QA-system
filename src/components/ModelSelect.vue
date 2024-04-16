<script setup>
import { defineProps, defineEmits, ref } from 'vue'
import {knowledgebaseGetKBListService} from "@/api/knowledgebase.js";
import {useUserStore} from "@/stores/index.js";
import KBEdit from "@/components/KBEdit.vue";
import {modelGetModelListService} from "@/api/model.js";

defineProps({
  modelValue:{
    type: Number
  }
})

const emit = defineEmits('update:modelValue')

const modelList = ref([])
const userStore = useUserStore()

// 添加知识库
const getModelList = async () => {
  try {
    // 调用 modelGetModelListService 获取历史会话信息
    console.log('modelGetModelListService is running')
    const response = await modelGetModelListService({userid: userStore.token.id});
    modelList.value = response.modellist;
    console.log('modellist', modelList)
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取模型列表失败，请重试！');
    console.error('Error fetching ModelList:', error);
  }
};
getModelList()



</script>

<template>
  <el-select
      :model-value="modelValue"
      @update:modelValue="emit('update:modelValue', $event)"
  >
    <el-option
        v-for="item in modelList"
        :key="item.modelid"
        :label="item.modelname + ' ' + item.timestamp"
        :value="item.modelid"
    >
    </el-option>
    <el-option
        :label="'不选择'"
        :value="null"
    >
    </el-option>
  </el-select>
</template>

<style scoped>

</style>
<script setup>
import { defineProps, defineEmits, ref } from 'vue'
import {knowledgebaseGetKBListService} from "@/api/knowledgebase.js";
import {useUserStore} from "@/stores/index.js";
import KBEdit from "@/components/KBEdit.vue";

defineProps({
  modelValue:{
    type: Number
  }
})

const emit = defineEmits('update:modelValue')

const kblist = ref([])
const userStore = useUserStore()
const dialog = ref();

// 添加知识库
const onAddKB = () => {
  console.log('onAddKB')
  dialog.value.openDialog()
}


const getKBList = async () => {
  try {
    // 调用 knowledgebaseGetKBListService 获取历史会话信息
    console.log('knowledgebaseGetKBListService is running')
    const response = await knowledgebaseGetKBListService({userId: userStore.token.id});
    kblist.value = response.kblist;
    console.log('kblist',kblist)
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取知识库列表失败，请重试！');
    console.error('Error fetching KBList:', error);
  }
};
getKBList()



</script>

<template>
  <el-select
      :model-value="modelValue"
      @update:modelValue="emit('update:modelValue', $event)"
  >
    <el-option
        v-for="item in kblist"
        :key="item.kbid"
        :label="item.kbname"
        :value="item.kbid"
    >
    </el-option>
    <el-option
        :label="'不选择'"
        :value="null"
    >
    </el-option>
    <template #footer>
      <el-button style="border: none; width: 100%" @click="onAddKB">
        添加知识库
        <template #icon>
          <i-ep-plus />
        </template>
      </el-button>
    </template>
  </el-select>
  <KBEdit ref="dialog" @success="getKBList"></KBEdit>
</template>

<style scoped>

</style>
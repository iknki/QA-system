<script setup>
import {onMounted, watch, ref} from 'vue';
import PageContainer from "@/components/PageContainer.vue";
import UserEdit from "@/components/UserEdit.vue";
import {useUserStore} from "@/stores/index.js";
import {userDeleteUserService, userGetUserListService} from "@/api/user.js";

const table_loading = ref(false);
const userStore = useUserStore()
const userList = ref([])
const total = ref(0) // 总数
const userEditRef = ref() // 编辑组件引用

// 定义查询参数
const params = ref({
  pagenum: 1, // 当前页码
  pagesize: 5, // 每页显示条数
})

// 获得知识列表
const getUserList = async() => {
  try {
    table_loading.value = true;
    // 调用 userGetUserListService 获取用户列表
    console.log('userGetUserListService is running')
    const response = await userGetUserListService(params.value);
    // 更新用户列表
    userList.value = response.users;
    // 更新总数
    total.value = response.total;
    console.log('UserList',userList)
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取用户列表失败，请重试！');
    console.error('Error fetching UserList:', error);
    table_loading.value = false;
  }
}



// 添加知识
const onAddUser = () => {
  console.log('onAddUser')
  userEditRef.value.openDialog()
}

// 编辑知识
const onEditUser = (row) => {
  console.log('onEditUser')
  userEditRef.value.openDialog(row)
}

// 删除逻辑
const onDeleteUser = async (row) => {
  console.log('onDeleteUser')
  await ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  try {
    console.log('onDeleteUser')
    const response = await userDeleteUserService({userid: row.userid});
    ElMessage.success(response.message)
    console.log('Success Delete User')
    getUserList()
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('删除用户失败:', error.message);
    console.error('Error Delete User:', error);
  }
}

onMounted( () => {
  getUserList()
})

watch(params, () => {
      getUserList()
    }, {deep: true}
)

// 成功回调
const onSuccess = () => {
  getUserList()
}

</script>

<template>
  <el-main>
    <page-container title="知识管理">
      <template #extra>
        <el-button type="primary" @click="onAddUser">
          添加用户
          <template #icon>
            <i-ep-plus />
          </template>
        </el-button>
      </template>
      <!-- 表格区域 -->
      <el-table :data="userList" style="width: 100%" v-loading="table_loading">
        <el-table-column type="index" label="序号" width="60px" align="center">
          <template #default="{ $index }">
            {{ $index + params.pagesize * (params.pagenum - 1) + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="用户id" prop="userid" align="center"></el-table-column>
        <el-table-column label="用户名" prop="username" align="center"></el-table-column>
        <el-table-column label="用户密码" prop="password" align="center"></el-table-column>
        <el-table-column label="状态" prop="role" align="center">
          <template #default="{row}">
            <el-tag v-if="row.role==='admin'" type="success">管理员</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="timestamp" align="center"></el-table-column>
        <el-table-column label="操作" width="100px" align="center">
          <template #default="{row, $index}">
            <el-button type="primary" circle plain @click="onEditUser(row)">
              <el-icon >
                <i-ep-edit />
              </el-icon>
            </el-button>
            <el-button type="danger"  circle plain @click="onDeleteUser(row)">
              <el-icon >
                <i-ep-delete />
              </el-icon>
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无数据"></el-empty>
        </template>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
          v-model:current-page="params.pagenum"
          v-model:page-size="params.pagesize"
          :page-sizes="[3, 5, 7, 10, 15, 20]"
          :background="true"
          layout="jumper, total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"

      />
    </page-container>
    <!-- 编辑组件 -->
    <UserEdit ref="userEditRef" @success="onSuccess"/>
  </el-main>
</template>

<style scoped>
.limited-text {
  max-height: 8em; /* 设置最大高度 */
  overflow: hidden; /* 隐藏溢出内容 */
  display: -webkit-box; /* 使用 flexbox 布局模型 */
  -webkit-line-clamp: 8; /* 设置最大行数 */
  -webkit-box-orient: vertical; /* 垂直方向布局 */
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}

</style>
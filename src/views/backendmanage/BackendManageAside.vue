<script setup>


</script>

<template>
  <el-aside width="isCollapse" class="session-panel">
    <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="transparent"
        router
    >
      <h1 class="title" v-if="!isCollapse">知识库管理</h1>
      <el-sub-menu index="/backendmanage/kbmanage">
        <template #title>
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-title">知识库管理</span>
        </template>
        <el-menu-item index="/backendmanage/kbmanage/kblist">
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-item">知识库列表</span>
        </el-menu-item>
        <el-menu-item index="/backendmanage/kbmanage/knowledgelist">
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-item">知识管理</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/backendmanage/model">
        <template #title>
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-title">问题推荐模型</span>
        </template>
        <el-menu-item index="/backendmanage/model/test">
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-item">模型测试</span>
        </el-menu-item>
        <el-menu-item index="/backendmanage/model/train">
          <el-icon><i-ep-document /></el-icon>
          <span class="menu-item">模型训练</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/backendmanage/logs">
        <el-icon><i-ep-document/></el-icon>
        <span class="menu-title">日志管理</span>
      </el-menu-item>
      <el-menu-item index="/backendmanage/settings">
        <el-icon><i-ep-document/></el-icon>
        <span class="menu-title">系统设置</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style scoped>

.el-menu {

  border: 0 !important;

}


.session-panel {
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  padding: 20px;
  position: relative;
  border-right: 1px solid rgba(0, 0, 0, 0.07);
  background-color: rgb(231, 248, 255);
  border: 0 !important;
}

.title {
  display: flex;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
}


.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
}

.menu-title {
  font-size: large;
}

.menu-item {
  font-size: medium;
}

</style>
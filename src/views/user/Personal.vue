<script setup>
import {useUserStore} from "@/stores/index.js";
import router from "@/router/index.js";

const userStore = useUserStore()

const logout = async () => {
  await ElMessageBox.confirm('你是否要退出', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  userStore.logout()
  router.push('/login')
}


</script>

<template>
  <!--  侧边栏  -->
  <el-container>
    <el-aside class="aside-container">
      <el-card class="person_body_left">
        <div slot="header" class="clearfix">
          <span class="person_body_list" style="border-bottom: none">个人中心</span>
        </div>
        <el-menu
            :default-active="$route.path"
            class="el-menu-vertical-demo"
            router
        >
          <el-menu-item
              index="/user/info"
          >
            <span class="menu-item" style="display: flex"> <i-ep-HomeFilled style="margin: auto"/> 个人信息</span>
          </el-menu-item>
          <el-menu-item
              index="/user/editPassword"
          >
            <span class="menu-item" style="display: flex"> <i-ep-EditPen style="margin: auto"/> 重置密码</span>
          </el-menu-item>
          <el-menu-item
              @click="logout"
          >
            <span class="menu-item" @click="logout" style="display: flex"> <i-ep-SwitchButton style="margin: auto"/> 退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-card>
    </el-aside>
    <!--  主题  -->
    <el-main>
      <router-view/>
    </el-main>
  </el-container>
</template>

<style lang="scss" scoped>

.el-menu {

  border: 0 !important;

}

.menu-item {
  font-size: 16px;
  margin: 0 auto;
}


.aside-container {
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  padding: 20px;
  border: 0 !important;
  margin-left: 5vw;
}

.person_body_left {
  width: 100%;
  height: 80vh;
  border-radius: 5px;
  margin-right: 3%;
  text-align: center;
}

.person_body_list {
  width: 100%;
  height: 50px;
  margin-top: 25px;
  font-size: 22px;
  border-bottom: 1px solid #f0f0f0;
  background-image: -webkit-linear-gradient(
      left,
      rgb(42, 134, 141),
      #e9e625dc 20%,
      #3498db 40%,
      #e74c3c 60%,
      #09ff009a 80%,
      rgba(82, 196, 204, 0.281) 100%
  );
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  -webkit-background-size: 200% 100%;
  -webkit-animation: masked-animation 4s linear infinite;
}

.el-menu-item {
  margin-top: 22px;
}


</style>
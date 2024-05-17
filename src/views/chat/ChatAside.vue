<script setup>
import {inject, onMounted, onBeforeUnmount, ref} from 'vue';
import SessionItem from "@/components/SessionItem.vue";
import {CircleClose} from "@element-plus/icons-vue";
import {useUserStore, chatBufferStore} from "@/stores/index.js";
import {sessionGetSessionListService, sessionCreateSessionService, sessionDeleteSessionService} from "@/api/session.js";

const isCollapse = ref(false);
const userStore = useUserStore()
const sessions = ref([])
const active = ref(0)
const selected_sessionId = inject('selected_sessionId')

const isbutton = ref(true)
const NewSessionName = ref('')
const collapse = () => {
  isCollapse.value = !isCollapse.value;
}

const handleSelectSession = (sessionid) => {
  selected_sessionId.value = sessionid
}

const handleCreateSession = async () => {
  isbutton.value = false
  isCollapse.value = false
}

const CreatNewSession = async () => {
  console.log('CreatNewSession')
  const response = await sessionCreateSessionService({
    userId: userStore.token.id,
    sessionname: NewSessionName.value
  });
  console.log('CreatNewSession Success')
  NewSessionName.value = ''
  sessions.value.push(response.session);
  isbutton.value = true
}

const DeleteSession = async (sessionid) => {
  console.log('DeleteSession')
  await ElMessageBox.confirm('此操作将永久删除该会话历史记录, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  const response = await sessionDeleteSessionService({
    sessionId: sessionid,
    userId: userStore.token.id
  });
  console.log('DeleteSession Success')
  ElMessage.success(response ? response.message : '删除成功')
  sessions.value = sessions.value.filter(session => session.sessionid !== sessionid)
}

const CancelCreatNewSession = () => {
  console.log('CancelNewSession')
  NewSessionName.value = ''
  isbutton.value = true
}

// 初始化
const Init = async () => {
  try {
    // 调用 chatGetSessionListService 获取历史会话信息
    console.log('sessionGetSessionListService is running')
    const response = await sessionGetSessionListService({userId: userStore.token.id});
    sessions.value = response.sessions;
    // 如果成功获取到历史对话信息，则更新 messages 变量
    console.log(sessions)
    if (sessions.value.length === 0) {
      console.log('sessionCreateSessionService is running')
      const response = await sessionCreateSessionService({
        userId: userStore.token.id,
        sessionname: '新会话1'
      });
      console.log(sessions)
      sessions.value.push(response.session);
    }
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取历史会话信息失败，请重试！');
    console.error('Error fetching SessionList:', error);
  }
  console.log('Success fetching SessionList')
  active.value = sessions.value[0].sessionid
  selected_sessionId.value = sessions.value[0].sessionid
}

onMounted(() => {
  const bufferStore = chatBufferStore()
  if(bufferStore.sessions.length === 0){
    Init()
  }
  else {
    sessions.value = bufferStore.sessions.value
    active.value = selected_sessionId.value
  }
})

onBeforeUnmount(() => {
  const bufferStore = chatBufferStore()
  bufferStore.sessions.value = sessions.value
  console.log('缓存成功')
  console.log(bufferStore.sessions.value)
})

</script>

<template>
  <el-aside width="isCollapse" class="session-panel">
    <el-menu
        :default-active="''+active"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        :collapse-transition="true"
        background-color="transparent"
    >
      <h1 class="title" v-if="!isCollapse">历史记录</h1>
      <el-menu-item class="session-item"
                    v-for="session in sessions"
                    :index="''+session.sessionid"
                    @click="handleSelectSession(session.sessionid)"
                    v-if="!isCollapse"
      >
        <template #title>
          <div class="mask"></div>
          <h1 class="name">{{ session.sessionname }}</h1>
          <div class="count-time">
            <div class="time">{{ session.createtime }}</div>
          </div>
        </template>
        <div class="btn-wrapper">
          <el-icon :size="30" class="close" @click="DeleteSession(session.sessionid)">
            <CircleClose/>
          </el-icon>
        </div>
      </el-menu-item>
      <!--  新建会话按钮-->
      <div style="margin-top: 20px" v-if="!isCollapse">
        <el-button type="primary"
                   round class="createsession-button"
                   v-if="isbutton"
                   @click="handleCreateSession"
        >
          新建会话
        </el-button>
        <div v-else>
          <el-input
              v-model="NewSessionName"
              placeholder="输入新会话名"
              @keyup.enter.native="CreatNewSession"
          >
          </el-input>
          <el-button type="success" circle plain @click="CreatNewSession">
            <el-icon>
              <i-ep-check/>
            </el-icon>
          </el-button>
          <el-button type="danger" circle plain @click="CancelCreatNewSession">
            <el-icon>
              <i-ep-close/>
            </el-icon>
          </el-button>

        </div>
      </div>
      <!--  收缩侧边栏 -->
      <div
          style="display: flex; flex-direction: column; justify-content: center; align-items: center;width:100%"
          v-if="isCollapse"
      >
        <i-ep-Comment style="margin-top: 10vh; margin-bottom: 40px; font-size: 40px; color: #5274F3"/>
        <el-button style="border: none; padding: 0" type="primary" circle @click="handleCreateSession">
          <el-tooltip
              placement="bottom"
              content="新建会话"
              trigger="hover"
              :width="10"
          >
            <i-ep-plus style="color: #5274F3; font-size: 20px"/>
          </el-tooltip>
        </el-button>
      </div>
    </el-menu>
  </el-aside>

  <!--  折叠按钮-->
  <div style="align-items: center; display: flex ">
    <el-button class="collapse-btn" left="isCollapse" @click="collapse">
      <el-icon v-if="isCollapse" style="color: #626aef">
        <i-ep-DArrowRight/>
      </el-icon>
      <el-icon v-else style="color: #626aef">
        <i-ep-DArrowLeft/>
      </el-icon>
    </el-button>
  </div>
</template>

<style scoped>

.el-menu {

  border: 0 !important;

  div {
    display: flex;
    .el-button+.el-button {
      margin-left: 0;
    }
  }

}



.title {
  display: flex;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  margin-top: 40px;
}

.session-panel {
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  padding: 0;
  position: relative;
  border-right: 1px solid rgba(0, 0, 0, 0.07);
  background-color: rgb(231, 248, 255);
  position: relative;
  border: 0 !important;
}

.session-item {

  /* 加一下padding不要让会话内容靠边界太近 */
  margin-top: 10px;
  margin-bottom: 10px;
  padding: 12px;
  background-color: white;
  /* 给边界一些圆角看起来圆润一些 */
  border-radius: 10px;
  border: black;
  /* 当鼠标放在会话上时改变鼠标的样式，暗示用户可以点击。目前还没做拖动的效果，以后会做。 */
  cursor: grab;
  /* 父相子绝，父元素是相对布局的情况下，子元素的绝对布局是相当于父元素绝对布局。 */
  position: relative;
  /* 子元素的遮罩一开始会在外面，让溢出的遮罩不显示 */
  overflow: hidden;


  .name {
    /* 会话名称字体要大一些 */
    font-size: 14px;
    /* 凸显名称，加粗 */
    font-weight: 700;
    width: 100vw;
    /* 加粗后颜色淡一些 */
    color: rgba(0, 0, 0, 0.8);
  }

  .count-time {
    /* 增加一些距离 */
    margin-top: 10px;
    /* 让字体小一些不能比会话名称要大（14px） */
    font-size: 10px;
    color: rgba(0, 0, 0, 0.5);
    /* 让消息数量和最近更新时间显示水平显示 */
    display: flex;
    /* 让消息数量和最近更新时间分布在水平方向的两端 */
    justify-content: space-between;
  }

  /* 当处于激活状态时增加蓝色描边 */

  &.is-active {
    /* 增加一些过渡 */
    transition: all 0.12s linear;
    border: 2px solid #1d93ab;
  }

  /* 当鼠标放在会话上时触发下面的css样式*/

  &:hover {
    /* 遮罩入场，从最左侧滑进去，渐渐变得不透明 */

    .mask {
      opacity: 1;
      left: 0;
    }

    .btn-wrapper {
      /* 暗示用户这个按钮可以点击 */

      &:hover {
        cursor: pointer;
      }

      /* 按钮入场，从最右侧滑进去，渐渐变得不透明 */
      opacity: 1;
      right: 20px;
    }
  }

  .mask {
    /* 渐变样式 */
    transition: all 0.2s ease-out;
    /* 相当于父亲绝对布局 */
    position: absolute;
    background-color: rgba(0, 0, 0, 0.05);
    /* 和父亲元素一样宽盖住父元素 */
    width: 100%;
    /* 和父亲元素一样高 */
    height: 100%;
    /*位置移到父元素的最上面 */
    top: 0;
    /* 向父元素的最左侧再增加一个父亲元素当前宽度的距离 */
    left: -100%;
    /* 透明度为0 */
    opacity: 0;
  }

  /* 删除按钮样式的逻辑和mask类似 */

  .btn-wrapper {
    color: rgba(0, 0, 0, 0.5);
    transition: all 0.2s ease-out;
    position: absolute;
    right: -20px;
    z-index: 10;
    opacity: 0;

    .edit {
      margin-right: 5px;
    }
  }
}


.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 240px;
  padding-left: 10px;
  margin: 0;
}

.collapse-btn {
  position: absolute;
  font-size: 20px;
  border: none;
  background-color: #f4f6fa;
}

.collapse-btn:hover {
  background-color: #f4f6fa;
}

.createsession-button {
  display: flex;
  margin: 0 auto;
}
</style>
<template>
  <el-container class="app_container">
    <el-main>
      <router-view/>
    </el-main>
    <el-footer>
      <nav-bar class="bottom_nav"></nav-bar>
    </el-footer>
  </el-container>
</template>

<script>
import NavBar from './components/public/NavBar.vue'

export default {
  name: 'App',

  components: {
    NavBar,
  },

  data: () => ({
    //
  }),
}
</script>
<style scoped>
.app_container{
  height: 100%;
  font-family: "Microsoft YaHei";
}
.bottom_nav{
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}
</style>
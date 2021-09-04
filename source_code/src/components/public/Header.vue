<template>
    <header class="head_container">
        <el-row class="header" :style="'height:'+ height">
            <el-col>
                <span class="page-title">{{pageTitle}}</span><slot></slot>
            </el-col>
        </el-row>
    </header>
</template>

<script>

export default {
  name: 'AppHeader',
  props: {
      "pageTitle": {default: 'title'},
      "height": {default: "64px"}
  },

}

</script>
<style scoped>
.header{
    align-content: center;
    padding: 16px;
    background-color: #FF9800;
    color: #fff;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    width: 100%;
}
.head_container{
    margin-bottom: 64px;
}

</style>
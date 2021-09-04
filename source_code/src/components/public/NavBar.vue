<template>
    <nav>
        <el-menu
        class="app_menu"
        router
        mode="horizontal"
        background-color="#FF9800"
        text-color="#fff"
        active-text-color="#FFE0B2">
        <template v-for="item in items" :key="item.title">
            <el-menu-item :index="item.link">
                <span style="font-size:24px" :class="item.icon">
                </span>
                {{item.title}}
            </el-menu-item>
        </template>
        </el-menu>
    </nav>
</template>

<script>
import { reactive } from 'vue'
import { Edit } from '@element-plus/icons'
export default {
  name: 'NavBar',
  components: {
      // eslint-disable-next-line vue/no-unused-components
      Edit,
  },
  setup(){
    let {items} = nav_items()
    return {items}
  },
}
function nav_items(){
    let items = reactive([
        {title: '日程管理', link: '/schedule_edit', icon: 'el-icon-edit'},
        {title: '视图', link: '/calendar_view', icon: 'el-icon-date'},
        {title: '记事本', link: '/notebook', icon: 'el-icon-notebook-2'}
    ])
    return {items}
}
</script>
<style scoped>
.app_menu{
    display: flex;
    justify-content: center;
}
.menu_item{
    display: flex;
    align-content: center;
}
</style>
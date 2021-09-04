<template>
<app-header class="top_header" page-title="日程管理" height="64px"></app-header>
<div v-if="loaded">
  <el-row class="table_row">
    <el-col :span = 5>
      事件
    </el-col>
    <el-col :span = 5>
      开始
    </el-col>
    <el-col :span = 5>
      结束
    </el-col>
    <el-col :span = 3>
      颜色
    </el-col>
    <el-col :span = 4>
      操作
    </el-col>
  </el-row>
  <el-row class="table_row" v-for="event, e_i in events" :key="e_i">
    <el-col :span = 5>
      {{ event.title }}
    </el-col>
    <el-col :span = 5>
      {{ event.start_date.toLocaleString() }}
    </el-col>
    <el-col :span = 5>
      {{ event.end_date.toLocaleString() }}
    </el-col>
    <el-col :span = 3 :style="'background-color:' + event.tl_color">
    </el-col>
    <el-col :span = 4>
      <el-button class="showBtn" @click="showEdit(e_i)"
        ><i class="el-icon-edit el-icon--right"></i
      ></el-button>
      <el-button class="deleteBtn" @click="deleteEvent(e_i)"
        ><i class="el-icon-delete el-icon--right"></i
      ></el-button>
    </el-col>
  </el-row>
</div>
  <el-dialog title="编辑"  width="100%" v-model="edit_table_visible">
    <edit-form @TableDataHandler="getTableData" :event="editing_id == -1 ? 'default' : events[editing_id]"/>
  </el-dialog>
  <el-button class="add_button" @click="showEdit()" circle><i class="el-icon-plus"></i></el-button>
</template>

<script>
import EditForm from './EditForm.vue'
import AppHeader from '../public/Header.vue'
import {ref, reactive} from 'vue'
import axios from 'axios'
export default {
  name: 'ScheduleEdit',
  components: {
    AppHeader,
    EditForm
  },
  setup(){
    const api_path = 'http://123.57.142.230:5001'
    let edit_table_visible = ref(false)
    let editing_id = ref(-1)
    let loaded = ref(false)
    let events = reactive([])
    axios.get(api_path+'/getAll')
    .then(res => {
      for(let e of res.data){
        events.push({
          'id': e.idnum,
          'title': e.event,
          'start_date': new Date(e.startTime),
          'end_date': new Date(e.endTime),
          'tl_color': e.color
        })
        if(!loaded.value) loaded.value = true
      }
    })
    function showEdit(id = -1){
      editing_id.value = id
      edit_table_visible.value = true
    }
    function deleteEvent(id){
      axios.delete(api_path + '/delete/' + events[id].id.toString())
      .then(()=>{
        events.splice(id, 1)
      })
    }
    function getTableData(d){
      edit_table_visible.value = false
      if(editing_id.value == -1){
        axios.post(api_path + '/addInfo', {
          "event": d.title,
          "start_time": d.start_date,
          "end_time":d.end_date,
          "color": d.tl_color
        })
        .then((res)=>{
          d.id = parseInt(res.data)
          events.push(d)
        })
      }else{
        events[editing_id.value] = d
        console.log(d)
        axios.put(api_path + '/update/' + events[editing_id.value].id.toString(), {
          "update_event": d.title,
          "update_start_time": d.start_date,
          "update_end_time":d.end_date,
          "update_color": d.tl_color
        })
      }
    }
    return {edit_table_visible, editing_id, events, loaded, showEdit, getTableData, deleteEvent}
  }
}
</script>
<style scoped>
.table_row{
  border-top: 2px solid #BDBDBD;
  margin: 0px -1px -1px 0px ;
  padding: 2px;
}
.table_row .el-col{
  margin: 2px;
  align-items: center;
  justify-content: center;
  display: flex;
}
.add_button{
  border-color: none;
  background-color: #FFEB3B;
  position: fixed;
  bottom: 68px;
  right: 12px;
}
.deleteBtn{
  border-color: none;
  background-color: #ec0800;
  color: white;
}
.showBtn{
  border-color: none;
  background-color: #ffaa3b;
  color: white;
}
</style>
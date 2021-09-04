<template>
  <el-form :model="formItems" :rules="rules" ref="form" label-position="top" label-width="80px">
  <el-form-item label="事件" prop="title"> 
    <el-input v-model="formItems.title" placeholder="请输入事件"></el-input>
  </el-form-item>
  <el-form-item label="起止时间" prop="dates">
    <el-date-picker
      v-model="formItems.dates"
      type="datetimerange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期">
    </el-date-picker>
  </el-form-item>
  <el-form-item label="背景颜色" prop="tl_color">
    <el-color-picker v-model="formItems.tl_color"></el-color-picker>
  </el-form-item>
  <el-row justify="center">
    <el-col :xs="24" :sm="12">
    <el-button style="width:100%" @click="submit_form()">提交</el-button>
    </el-col>
  </el-row>
</el-form>
</template>

<script>
import {ref, reactive, watch} from 'vue'
export default {
  emits: ['TableDataHandler'],
  name: 'EditForm',
  props: {
    'event': {
      default: {
        id: '-1',
        title: '',
        start_date: null,
        end_date: null,
        tl_color: '#' + ('00000' + (Math.random() * 0x1000000 << 0).toString(16)).substr(-6)
      }
    }
  },
  setup(props, { emit }){
    const form = ref(null)
    let formItems = reactive({
        'id': props.event.id,
        'title': props.event.title,
        'dates': reactive([props.event.start_date, props.event.end_date]),
        'tl_color': props.event.tl_color
    })
    watch(
      () => props.event,
      (newValue) => {
        formItems.title = newValue.title
        formItems.tl_color = newValue.tl_color
        formItems.id = newValue.id
        if(newValue.dates){
          formItems.dates[0] = newValue.dates[0] ? newValue.dates[0] : null
          formItems.dates[1] = newValue.dates[1] ? newValue.dates[1] : null
        }
      }
    )
    function submit_form(){
        if(formItems.dates[0] == formItems.dates[1]){
          alert('起止时间不能相同')
          return false
        }
        form.value.validate((valid) => {
          if (valid) {
            emit('TableDataHandler', {
              'id': formItems.id,
              'title': formItems.title,
              'start_date': formItems.dates[0],
              'end_date': formItems.dates[1],
              'tl_color': formItems.tl_color
            })
          } else {
            console.log('error submit!!');
            return false;
          }
          
      })
    }
    let rules = reactive({
        title: [
          { required: true, message: '请填写日程内容', trigger: 'blur' }
        ],
        dates: [
          { required: true, message: '请选择日期', trigger: 'change' }
          ],
        tl_color: [
          { required: true, message: '请选取颜色', trigger: 'blur' }
        ]
    })
    return {formItems, rules, form, submit_form}
  }, 
}

</script>
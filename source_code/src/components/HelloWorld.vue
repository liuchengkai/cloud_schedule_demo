<template>
  <el-row>
    <el-button type="primary">主要按钮</el-button>
  </el-row>
</template>

<script>
import {ref} from 'vue'

export default {
  name: 'HelloWorld',
  setup(){
    let {test_num, addNum} = test_fn()
    return {test_num, addNum}
  }
}
function test_fn(){
  let test_num = ref(0)
  function addNum(){
    test_num.value ++
  }
  return {test_num, addNum}
}
</script>

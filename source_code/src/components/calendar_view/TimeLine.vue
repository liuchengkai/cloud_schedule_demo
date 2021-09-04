<template>
  <div class="time_line" :style="'background-color: ' + tl_color + '; width: ' + width"><div class="tl_content"><slot></slot></div></div>
</template>

<script>
export default {
  name: 'TimeLine',
  props: {
      "width": {
          default: '100%'
      },
      "tl_color": {
          default: 'blue'
      },
  }
}
</script>
<style scoped>
.time_line{
    background-color: salmon;
    height: 28px;
    padding: 0px;
    margin: 0px;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
    z-index: 99;
}
.tl_content{
    padding: 4px;
}
</style>
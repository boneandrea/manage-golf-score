<template>
  <div class="sidebar-container">
    <h1><a href="/">G+ ゴルフデータ管理</a></h1>
    <navlist @receive="recv"></navlist>
  </div>
</template>
<script setup>
import Navlist from './Navlist.vue'
const emit = defineEmits(['receive'])
const recv = (data) => {
  emit('receive', data)
}
</script>
<style>
.sidebar-container {
  min-width: 200px;
  width: 80%;
  background: #fff;
  border-right: 1px solid #40b983;
}
.sidebar-container h1 {
  border-bottom: 1px solid #40b983;
  padding: 20px 0;
  color: #40b983;
}
</style>

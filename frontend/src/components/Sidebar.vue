<template>
  <div class="sidebar-container">
    <h1>G+ ゴルフデータ管理</h1>
    <navlist> </navlist>
  </div>
</template>
<script setup>
import Navlist from './Navlist.vue'
</script>
<style>
.sidebar-container {
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

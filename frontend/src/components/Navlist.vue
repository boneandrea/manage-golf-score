<template>
  <div>
    <nav class="nav-list-wrapper">
      <ul class="nav-list">
        <li class="nav-list-item" @click="newScore"><a href="#">新規入力</a></li>
        <li class="nav-list-item" @click="editScore"><a href="#">過去データ修正</a></li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2024" target="_blank">2024</a>
        </li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2025" target="_blank">2025</a>
        </li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2026" target="_blank">2026</a>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script setup>
import Navlist from './Navlist.vue'
const newScore = (e) => {
  console.log(e)
  alert(1)
}
const editScore = (e) => {
  console.log(e)
  alert(2)
}
</script>
<style>
.nav-list-wrapper {
  padding: 10px;
}
.nav-list-item {
  list-style: none;
  padding: 8px 0;
}
.nav-list-item a {
  color: #40b983;
  text-decoration: none;
  display: inline-block;
  width: 100%;
  font-size: 16px;
  font-weight: 700;
}
.nav-list-item a:hover {
  background: #40b983;
  opacity: 0.8;
  color: #fff;
}
</style>

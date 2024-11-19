<template>
  <div>
    <nav class="nav-list-wrapper">
      <ul class="nav-list">
        <li class="nav-list-item" @click="newScore"><a href="#">新規入力</a></li>
        <li class="nav-list-item" @click="editScore">
          <a href="#">過去データ修正</a>
          <DateList @receive="recv" class="ml-auto" :dateList="dateList"></DateList>
        </li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2024" target="_blank">2024</a>
        </li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2025" target="_blank">2025</a>
        </li>
        <li class="nav-list-item">
          <a href="https://boneandrea.github.io/gplus-golf-score/2026" target="_blank">2026</a>
        </li>
        <li class="nav-list-item">
          <a
            href="https://peixe.biz/junk/donguri/update_gplus_tour.php?key=ahv0doodinaefahv8Sahgee4ede1shee"
            target="_blank"
            @click="updateRanking"
            >ランキング更新</a
          >
        </li>
        <li class="nav-list-item">
          <a href="#" @click="download">download</a>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script setup>
import { ref, computed } from 'vue'
import Navlist from './Navlist.vue'
import DateList from './DateList.vue'
import { API_ROOT } from '@/utils/common'
import { HOLE, getPrize } from '@/utils/utils'
const emit = defineEmits(['receive'])
const showList = ref(false)
const dateList = ref([])
const newScore = (e) => {
  dateList.value.splice(0)
  emit('receive', { scores: [] })
}
const updateRanking = (e) => {
  if (!confirm('ランキングページを更新しますか？')) {
    e.preventDefault()
  }
}
const recv = (data) => {
  // par,古いデータはない
  if (!data.par) {
    console.log('set par: default')
    data.par = [...Array(HOLE)].map((_, i) => null)
  }
  console.log(data)
  emit('receive', data)
}
const editScore = (e) => {
  showList.value = !showList.value
  if (!showList.value) return

  const apiUrl = `${API_ROOT}/find`
  fetch(apiUrl, {
    method: 'GET',
    headers: { 'content-type': 'application/json' },
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      dateList.value.splice(0)
      data.forEach((d) => {
        dateList.value.push({
          date: d.date,
          id: d._id['$oid'],
          course: d.course,
        })
      })
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {})
}
const download = async (e) => {
  const apiUrl = `${API_ROOT}/download`
  const response = await fetch(apiUrl, {
    method: 'GET',
  })

  if (response.ok) {
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'golf.json'
    a.click()
  }
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

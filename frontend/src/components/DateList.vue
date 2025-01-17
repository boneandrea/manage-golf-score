<template>
  <ul>
    <li v-for="d in props.dateList" :key="d.id">
      <RouterLink to="/new" @click.stop.prevent="selectDate(d.id)">
        {{ formattedDate(d.date.$date) }}:
        {{ d.course }}
      </RouterLink>
    </li>
  </ul>
</template>
<script setup>
import { ref, computed } from 'vue'
import { API_ROOT } from '@/utils/common'
const props = defineProps(['dateList'])
const emit = defineEmits(['receive'])
const formattedDate = (d) => {
  const mydate = new Date(d)
  return `${mydate.getFullYear()}/${mydate.getMonth() + 1}/${mydate.getDate()}`
}
const selectDate = (id) => {
  const apiUrl = `${API_ROOT}/findOne/${id}`
  fetch(apiUrl, {
    method: 'GET',
    headers: { 'content-type': 'application/json' },
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      const d = new Date(data.date.$date)
      data.date = `${d.getFullYear()}-${d.getMonth() < 9 ? '0' : ''}${d.getMonth() + 1}-${d.getDate() < 10 ? '0' : ''}${d.getDate()}`
      emit('receive', data)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {})
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

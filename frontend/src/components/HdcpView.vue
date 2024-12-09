<script setup>
import { onMounted, defineEmits, ref, computed } from 'vue'
import { API_ROOT } from '@/utils/common'
const props = defineProps({
  members: Array,
})
// propsをコピーした値
const members = ref([])
onMounted(() => {
  fetchMembers()
})

const fetchMembers = () => {
  const apiUrl = `${API_ROOT}/members/`
  fetch(apiUrl, {
    method: 'GET',
    headers: { 'content-type': 'application/json' },
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
</script>
<template>
  <h1 class="green">HDCP管理</h1>
  <ul>
    <li v-for="m in members">
      {{ m.name }}
    </li>
  </ul>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}
th,
td {
  white-space: nowrap;
}
table {
  max-width: 800px;
}
@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
h1 {
  margin-top: 0.5em;
}
.edit-mode {
  width: 200px;
}

.form-group {
  margin-left: 10px;
}
.peria input {
  width: 6em;
}
.upload .btn {
  width: 200px;
}
</style>

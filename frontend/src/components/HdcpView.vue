<script setup>
import { onMounted, defineEmits, ref, computed } from 'vue'
import { API_ROOT } from '@/utils/common'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'
const $toast = useToast()
const props = defineProps({
  members: Array,
})

const items = ref([]) // propsをコピーした値
const items_org = [] // 初期値
onMounted(() => {
  fetchMembers()
})
const prize = ref([])

const newMember = ref({ name: '', hdcp: -100 })
const updateHdcp = (index) => {
  const player = items.value[index]
  const rank = prize.value[index]
  if (rank === '') {
    resetHdcp(index)
    return
  }
  if (rank === '1') {
    player.hdcp = Math.trunc(items_org[index].hdcp * 0.7)
    return
  }
  if (rank === '2') {
    player.hdcp = Math.trunc(items_org[index].hdcp * 0.8)
    return
  }
  if (rank === '3') {
    player.hdcp = Math.trunc(items_org[index].hdcp * 0.9)
    return
  }
}

const resetHdcp = (index) => {
  items.value[index].hdcp = items_org[index].hdcp
}
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
      data.forEach((d) => {
        items.value.push(d)
        items_org.push(structuredClone(d))
        prize.value.push(0)
      })
      console.log(items_org)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
const update = () => {
  const apiUrl = `${API_ROOT}/members/update`
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ members: items.value }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      $toast.success('更新しました')
      console.log(data)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
const add = () => {
  const apiUrl = `${API_ROOT}/members/add`
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ member: newMember.value }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      $toast.success('登録しました')
      newMember.value.name = ''
      newMember.value.hdcp = -100
      items.value.push(data)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
const remove = (_id, name) => {
  if (!confirm(`${name}: 削除してよいですか.戻せません`)) return
  if (!confirm(`${name}: 戻せません,OK?`)) return
  const id = _id['$oid']
  const apiUrl = `${API_ROOT}/members/remove`
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ member: { id } }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      $toast.success('削除しました')
      const removeIndex = items.value.findIndex((e) => e._id['$oid'] === id)
      items.value.splice(removeIndex, 1)
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
const download = () => {
  const apiUrl = `${API_ROOT}/download`
  fetch(apiUrl, {
    method: 'GET',
  })
    .then(async (response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
      const str = createCsv(data)
      const blob = new Blob([str], { type: 'text/csv' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = `fe.csv`
      link.click()
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
}
const createCsv = (members) => {
  let str = ''
  members.forEach((e) => {
    str += `${e.name},${e.hdcp}\n`
  })
  return str
}
</script>
<template>
  <div class="md-3">
    <h1 class="green">HDCP管理</h1>
    <hr />
    <h2>新規登録</h2>
    <div class="form-group row ml-1">
      <div class="name">
        <input v-model="newMember.name" class="form-control" placeholder="name" required />
      </div>
      <div>
        <input v-model="newMember.hdcp" class="form-control hdcp" type="number" step="1" placeholder="hdcp" required />
      </div>
      <button type="button" class="btn btn-primary" @click="add" :disabled="!newMember.name">追加</button>
    </div>
    <hr />
    <ul>
      <li v-for="(m, index) in items" :key="m.id">
        <div class="form-group ml-1">
          <div class="row">
            <div class="col name">
              {{ m.name }}
            </div>
            <div class="col">
              <input v-model.trim="m.hdcp" class="form-control hdcp" type="number" step="1" required />
            </div>
            <div class="col">
              <button type="form-control button" class="btn btn-danger" @click="remove(m._id, m.name)">削除</button>
              <select v-model="prize[index]" class="form-select" @change="updateHdcp(index)">
                <option></option>
                <option value="1">1位</option>
                <option value="2">2位</option>
                <option value="3">3位</option>
              </select>
            </div>
          </div>
        </div>
      </li>
    </ul>
    <div class="d-flex justify-content-between">
      <button type="button" class="mr-2 btn btn-primary" @click="update">更新</button>
      <button type="button" class="btn btn-secondary" @click="download">提出用HDCPダウンロード</button>
    </div>
  </div>
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
li {
  display: flex;
}
li input {
  display: inline-block;
}
li .name {
  display: flex;
  width: 16em;
  align-items: center;
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

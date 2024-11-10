<script setup>
import { ref, computed } from 'vue'
import { HOLE, getPrize } from '@/utils/utils'
import { API_ROOT } from '@/utils/common'
import ManualTable from './ManualTable.vue'
import DateList from './DateList.vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const msg = '本日のスコア'
const game = ref({})
const peria_holes = ref([...Array(HOLE)].map((_, i) => null))
const props = defineProps({
  data: Object,
})
const members = ref([])
const spinner0 = ref(false)
const spinner1 = ref(false)
const dateList = ref([])
const edit_mode = ref('url')
console.log(import.meta.env.MODE)
console.log(API_ROOT)

const collectPeriaHoles = () => {
  const check = {}
  peria_holes.value.forEach((e) => (check[e] = true))
  return Object.keys(check).length === 12
}
const incompletedPeriaHoles = computed(() => peria_holes.value.filter((e) => parseInt(e) > 0).length < 12)
const isDuplicated = (holeNo) => {
  let duplicated = false
  if (holeNo === '') return false

  return peria_holes.value.filter((e) => e === holeNo).length > 1
}
const inValidPeriaHole = (holeNo) => {
  // check重複
  const ee = parseInt(holeNo)
  const validationRange = !(ee > 0) || ee > 18
  const duplicated = isDuplicated(holeNo)
  return validationRange || duplicated
}

const title = computed(() => (edit_mode.value === 'url' ? 'URLから取得' : '地獄の手動入力'))
const readData = (date) => {
  const apiUrl = `${API_ROOT}/find`
  spinner0.value = true
  members.value.splice(0, members.value.length)
  fetch(apiUrl, {
    method: 'GET',
    headers: { 'content-type': 'application/json' },
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      edit_mode.value = 'manual'
      game.value.course = data[0].course
      game.value.date = new Date(data[0].date)
      const id = data[0]['_id']['$oid']
      dateList.value.splice(0)
      data.forEach((d) => {
        dateList.value.push({
          date: d.date,
          id: d._id['$oid'],
        })
      })
      data[0].scores.forEach((s) => {
        members.value.push(s)
      })
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {
      spinner0.value = false
    })
}
const fetchData = () => {
  if (!collectPeriaHoles()) {
    alert('新ペリホールを正しく指定してください')
    return
  }
  if (!q('#url').value) {
    alert('SET URL')
    return
  }
  const apiUrl = `${API_ROOT}/get`
  spinner0.value = true
  members.value.splice(0, members.value.length)
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      url: q('#url').value,
    }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
      game.value.course = data.course
      game.value.date = new Date(data.date)
      if (data.status === 'error') {
        throw new Error(data['reason'])
      }
      data['scores'].forEach((scores) => {
        scores.hdcp = calculateHDCP(scores)
        members.value.push(scores)
      })
      spinner0.value = false
      setNet()
      sort()
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {
      spinner0.value = false
    })
}

const changeTab = (name) => {
  edit_mode.value = name
}
const scoreByHole = (scores, hole_no) => {
  const s = scores.find((e) => e.hole === hole_no)

  return s ? s.score : 0
}
const calculateHDCP = (scores) => {
  //(隠しホールの合計スコアx1.5-72) x 0.8
  let sum = 0
  peria_holes.value.forEach((h) => {
    sum += scoreByHole(scores.score, parseInt(h))
  })

  return Math.round((sum * 1.5 - 72) * 0.8 * 100) / 100
}
const setNet = () => {
  members.value.forEach((e, i) => {
    members.value[i]['net'] = members.value[i]['gross'] - members.value[i]['hdcp']
  })
}

function change(e, i, nearPinIndex) {
  if (nearPinIndex === 0) members.value[i].near0 = true
  if (nearPinIndex === 1) members.value[i].near1 = true
  if (nearPinIndex === 2) members.value[i].near2 = true
  if (nearPinIndex === 3) members.value[i].near3 = true
}

const sort = () => {
  members.value.sort((a, b) => {
    if (a.net > b.net) return 1
    if (a.net < b.net) return -1
    if (a.gross > b.gross) return 1
    if (a.gross < b.gross) return -1
    return 0
  })

  members.value.forEach((e, i) => {
    e.point = members.value.length - i
  })
}

const dragIndex = ref(null)

function dragList(e, i) {
  console.log(e, i)
  console.log(members.value)
}

const dragStart = (index) => {
  console.log('drag start', index)
  dragIndex.value = index
}

const hdcp = (i) => {
  members.value[i].net = members.value[i].gross - members.value[i].hdcp
}

const dragEnter = (index) => {
  if (index === dragIndex) return
  const deleteElement = members.value.splice(dragIndex.value, 1)[0]
  members.value.splice(index, 0, deleteElement)
  dragIndex.value = index
}

const changeEdit = (e) => (edit_mode.value = e.target.value)

const create_data = (scores, par, nearpin) => {
  return scores.map((s) => {
    const personal_scores = s.score.map((ss, index) => ({
      hole: index + 1,
      prize: getPrize(par[index], ss),
      score: ss,
    }))
    const data = {
      name: s.name,
      score: personal_scores,
      gross: s.gross,
      hdcp: 0,
      net: 999,
      point: 999,
    }
    data.hdcp = calculateHDCP(data)
    members.value.push(data)
  })
}
const reset = () => {
  members.value.splice(0)
}
function updateManualData(score, par, courseInfo) {
  game.value.course = courseInfo.name
  game.value.date = new Date(courseInfo.date)
  members.value.splice(0)
  const data = create_data(score, par)
  setNet()
  if (!game.value.date) game.value.date = new Date()
  sort()
}

function send() {
  if (!confirm('送信してよいですか？')) return
  const apiUrl = `${API_ROOT}/store`
  spinner1.value = true
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      course: game.value.course,
      date: game.value.date,
      par: game.value.par,
      scores: members.value,
    }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
      if (data.status === 'error') {
        throw new Error(data['reason'])
      }
      spinner1.value = false
      alert('送信成功しました')
      members.value.splice(0, members.value.length)
      for (let key in game.value) {
        if (game.value.hasOwnProperty(key)) {
          delete game.value.key
        }
      }
      game.value.date = null
      localStorage.removeItem('golf-gplus')
    })
    .catch((e) => {
      spinner1.value = false
      console.error(e)
      alert(e)
    })
}
const setPeriaHoles = (holes) => {
  peria_holes.value.splice(0)
  holes.forEach((h) => peria_holes.value.push(h))
}
const today = new Date()
</script>
<template>
  <div>
    <h1 class="green">スコア登録</h1>
    <p>
      <a href="./pdf">download pdf(できてない)</a>
    </p>
    <h3 class="green">新ペリホール番号</h3>
    <div class="form-group row peria">
      <div v-for="(hole, index) in peria_holes.slice(0, 6)">
        <input
          class="form-control mr-2"
          :class="{ 'is-invalid': inValidPeriaHole(peria_holes[index]) }"
          type="number"
          v-model="peria_holes[index]"
          min="1"
          max="18"
          required
          v-bind:autofocus="index === 0"
        />
      </div>
    </div>
    <div class="form-group row peria" style="margineddc-left: 50px">
      <div v-for="(hole, index) in peria_holes.slice(6, 12)">
        <input
          class="form-control mr-2"
          :class="{ 'is-invalid': inValidPeriaHole(peria_holes[index + 6]) }"
          type="number"
          v-model="peria_holes[index + 6]"
          min="1"
          max="18"
          required
        />
      </div>
    </div>
    <h2 class="green">{{ title }}</h2>
    <div>
      <button @click="readData()">readOne</button>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: edit_mode === 'url' }" @click="changeTab('url')">
            <i class="bi bi-browser-chrome"></i>
            URL
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: edit_mode === 'manual' }" @click="changeTab('manual')">
            <i class="bi bi-pencil"></i>
            Manual
          </a>
        </li>
      </ul>
    </div>
    <div class="tab-content">
      <div class="tab-pane mt-2" :class="{ active: edit_mode === 'url' }" v-if="edit_mode === 'url'">
        <div class="form-group row">
          <div class="col">
            <input class="form-control" type="url" id="url" placeholder="スコアのURL" autofocus />
          </div>
          <div class="col">
            <button
              class="btn btn-primary"
              @click="fetchData"
              :disabled="incompletedPeriaHoles || spinner0 || spinner1"
            >
              データ取得
            </button>
          </div>
          <div class="col">
            <div v-show="spinner0" class="spinner-border text-secondary" role="status" />
          </div>
        </div>
      </div>
      <div class="tab-pane mt-2" :class="{ active: edit_mode === 'manual' }" v-if="edit_mode === 'manual'">
        <ManualTable
          class="ml-auto"
          @update-manual-data="updateManualData"
          @reset-manual-data="reset"
          @set-peria-holes="setPeriaHoles"
          :peria_holes="peria_holes"
          :score="props.score"
        />{{ props }}
      </div>
    </div>
    <hr />
    <h2 class="green">RESULT</h2>
    <h3 v-if="game.date" class="green">
      [{{ game.course }}] {{ game.date.getFullYear() }}/{{ game.date.getMonth() + 1 }}/{{ game.date.getDate() }}
    </h3>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>順位</th>
          <th>name</th>
          <th>ニアピン1-9</th>
          <th>ニアピン10-18</th>
          <th>gross</th>
          <th>HDCP</th>
          <th>NET</th>
          <th>獲得ポイント</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(member, index) in members"
          :draggable="true"
          @dragstart="dragStart(index)"
          @dragenter="dragEnter(index)"
        >
          <td>{{ index + 1 }}</td>
          <td>
            <input class="form-control responsive" type="text" style="min-width: 10em" v-model="member.name" />
          </td>
          <td>
            <input type="checkbox" @change="change(e, index, 0)" :checked="members[index].near0" />
            <input type="checkbox" @change="change(e, index, 1)" :checked="members[index].near1" />
          </td>
          <td class="col-xs-6">
            <input type="checkbox" @change="change(e, index, 2)" :checked="members[index].near2" />
            <input type="checkbox" @change="change(e, index, 3)" :checked="members[index].near3" />
          </td>
          <td>{{ member.gross }}</td>
          <td>{{ member.hdcp }}</td>
          <td>{{ member.net }}</td>
          <td>{{ member.point }}</td>
        </tr>
      </tbody>
    </table>
    <p>やること：</p>
    <ol>
      <li>名前修正</li>
      <li>ニアピン設定</li>
    </ol>
    <div class="form-group row upload">
      <div class="col">
        <button class="btn btn-primary" @click="send" :disabled="incompletedPeriaHoles || spinner0 || spinner1">
          <i class="bi bi-cloud-upload"></i>
          送信
        </button>
      </div>
      <div class="col">
        <div v-show="spinner1" class="spinner-border text-secondary" role="status" />
      </div>
    </div>
  </div>
  <hr />
  {{ data }}
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

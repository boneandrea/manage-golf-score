<script setup>
import { ref, watch, computed } from 'vue'
import { HOLE, getPrize } from '@/utils/utils'
import { API_ROOT } from '@/utils/common'
import ManualTable from './ManualTable.vue'
import DateList from './DateList.vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const msg = '本日のスコア'
const game = ref({})
const peria_holes = ref([...Array(HOLE)].map((_, i) => null))
const props = defineProps({
  data: Object({}),
})
const spinner0 = ref(false)
const spinner1 = ref(false)
const edit_mode = ref('url')
const rate = ref(1)
console.log(import.meta.env.MODE)
console.log(API_ROOT)

const page = () => {
  if (props.data._id) {
    return '修正'
  } else {
    return '登録'
  }
}

const remove = () => {
  if (!confirm('この日のデータを削除します。戻せません')) return
  const id = props.data._id.$oid
  const apiUrl = `${API_ROOT}/remove/${id}`
  spinner0.value = true
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({}),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      alert('削除しました')
      window.location.reload()
    })
    .finally(() => {
      spinner0.value = false
    })
}
watch(props, () => {
  if (props.data._id) {
    edit_mode.value = 'manual'
  }
  rate.value = props.data.rate || 1
})

const changeDate = (e) => (props.data.date = e)
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
      game.value.course = data.course
      game.value.date = new Date(data.date)
      rate.value = data.rate
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
  if (props.data._id) {
    alert('修正時は手動入力のみです')
    return
  }
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

const changeNearPin = (e, i, nearPinIndex) => {
  if (nearPinIndex === 0) props.data.scores[i].near0 = true
  if (nearPinIndex === 1) props.data.scores[i].near1 = true
  if (nearPinIndex === 2) props.data.scores[i].near2 = true
  if (nearPinIndex === 3) props.data.scores[i].near3 = true
}

const hdcp = (i) => {}

const dragIndex = ref(null)

const dragStart = (index) => {
  console.log('drag start', index)
  console.log(props.data.scores[index])
  dragIndex.value = index
}

const dragEnter = (index) => {
  if (index === dragIndex) return
  const deleteElement = props.data.scores.splice(dragIndex.value, 1)[0]
  props.data.scores.splice(index, 0, deleteElement)
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
  return
  game.value.course = courseInfo.name
  game.value.date = new Date(courseInfo.date)
  members.value.splice(0)
  const data = create_data(score, par)
  setNet()
  if (!game.value.date) game.value.date = new Date()
  sort()
}

function changeRate(v) {
  rate.value = v
}
function send() {
  if (!confirm('送信してよいですか？')) return
  if (!props.data.scores[0].point) {
    alert('ポイントが入っていません。Sortを押してください。')
    return
  }
  const content = {
    course: props.data.course,
    date: props.data.date,
    par: props.data.par,
    scores: props.data.scores,
    rate: rate.value,
  }
  if (props.data._id) {
    content.id = props.data._id.$oid
  }
  console.log(content)
  const apiUrl = props.data._id ? `${API_ROOT}/update` : `${API_ROOT}/store`

  spinner1.value = true
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(content),
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
    <h1 class="green">スコア{{ page() }}</h1>
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
          @update-manual-data="updateManualData"
          @reset-manual-data="reset"
          @set-peria-holes="setPeriaHoles"
          @change-date="changeDate"
          :peria_holes="peria_holes"
          :score="data"
        />
      </div>
    </div>
    <hr />
    <h2 class="green">RESULT</h2>
    <h3 v-if="data.date" class="green">[{{ data.course }}] / {{ data.date }}</h3>
    <div class="container">
      <div class="form-check">
        <input
          class="form-check-input"
          name="rate"
          type="radio"
          v-model="rate"
          id="flexRadioDefault1"
          value="1"
          @change="changeRate(1)"
        />
        <label class="form-check-label" for="flexRadioDefault1"> 1倍 </label>
      </div>
      <div class="form-check">
        <input
          class="form-check-input"
          type="radio"
          v-model="rate"
          value="2"
          name="rate"
          id="flexRadioDefault2"
          @change="changeRate(2)"
        />
        <label class="form-check-label" for="flexRadioDefault2"> 2倍 </label>
      </div>
    </div>
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
          v-for="(score, index) in data.scores"
          :draggable="true"
          @dragstart="dragStart(index)"
          @dragenter="dragEnter(index)"
        >
          <td>{{ index + 1 }}</td>
          <td>
            <input class="form-control responsive" type="text" style="min-width: 10em" v-model="score.name" />
          </td>
          <td>
            <input type="checkbox" @change="changeNearPin(e, index, 0)" :checked="score.near0" />
            <input type="checkbox" @change="changeNearPin(e, index, 1)" :checked="score.near1" />
          </td>
          <td class="col-xs-6">
            <input type="checkbox" @change="changeNearPin(e, index, 2)" :checked="score.near2" />
            <input type="checkbox" @change="changeNearPin(e, index, 3)" :checked="score.near3" />
          </td>
          <td>{{ score.gross }}</td>
          <td>{{ score.hdcp }}</td>
          <td>{{ score.net }}</td>
          <td>{{ score.point }}</td>
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
        <button class="btn btn-primary" @click="send">
          <i class="bi bi-cloud-upload"></i>
          送信
        </button>
      </div>
      <div class="col">
        <div v-show="spinner1" class="spinner-border text-secondary" role="status" />
      </div>
    </div>
    <div class="form-group row" v-if="props.data._id">
      <div class="col">
        <button type="button" class="btn btn-danger" @click="remove">
          <i class="bi bi-trash"></i>
          この日のデータを削除する（戻せません）
        </button>
      </div>
    </div>
  </div>
  <hr />
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

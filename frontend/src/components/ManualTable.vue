<script setup>
import { defineEmits, ref, computed } from 'vue'
import { HOLE, getPrize } from '@/utils/utils'
const props = defineProps({
  score: Object,
  peria_holes: Array,
})
const emit = defineEmits(['updateManualData', 'resetManualData', 'setPeriaHoles', 'changeDate'])
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const courseInfo = ref({ name: '', date: null })
const par = ref([...Array(HOLE)].map((_, i) => null))
const NEWUSER = {
  name: '',
  score: [...Array(HOLE)].map((_, i) => ({ hole: i, score: null })),
  gross: 0,
  hdcp: 0,
  net: 0,
}

// propsをコピーした値
const score = ref({
  peria_holes: [],
  score: {
    course: '',
    scores: [],
    date: '',
  },
})
const holes = [...Array(HOLE)].map((_, i) => i + 1)
const changeHdcp = (index) => {
  const target = score.value.score.scores[index]
  target.net = (Math.round((target.gross - parseFloat(target.hdcp)) * 10) / 10).toFixed(1)
}

const helpNearpin = () => {
  alert('ニアピンはRESULT画面で設定してください')
}

const dump = (player_index, hole_index, s) => {
  const target = score.value.score.scores[player_index]
  target.gross = target.score.reduce(function (sum, element) {
    return sum + element.score
  }, 0)

  changeHdcp(player_index)
  s.prize = getPrize(score.value.score.par[hole_index], target.score[hole_index].score)
  if (s.score > 10) {
    alert(`${s.score} も打った??\nマジですか????`)
  }
}
const sort = () => {
  if (!score.value.score.course) {
    alert('入力が完了していません')
    return
  }
  if (!score.value.score.date) {
    alert('入力が完了していません')
    return
  }
  score.value.score.scores.sort((a, b) => a.net - b.net)
  setPoint()
}
const setPoint = () => {
  const scores = score.value.score.scores
  scores.forEach((e, i) => {
    scores[i].point = scores.length - i
  })
}
const changeDate = (e) => emit('changeDate', e.target.value)
const addPlayer = () => score.value.score.scores.push(structuredClone(NEWUSER))
const removePlayer = (index) => {
  const scores = score.value.score.scores
  const name = score.value.score.scores[index].name
  if (!confirm(`${name} さんを消しますよ？？？OK?`)) return
  scores.splice(index, 1)
}

import { onMounted } from 'vue'

onMounted(() => {
  score.value = Object.assign(score.value, props)

  if (!score.value.score) {
    addPlayer()
  }
})
</script>
<template>
  <div>
    <form>
      <div class="form-group row ml-1">
        <input
          class="form-control w-25"
          :class="{ 'is-invalid': !score.score.course }"
          placeholder="コース名"
          v-model.trim="score.score.course"
          required
        />
      </div>
      <div class="form-group row ml-1">
        <input
          class="form-control w-25"
          :class="{ 'is-invalid': !score.score.date }"
          placeholder="日時"
          :value="score.score.date"
          type="date"
          @change="changeDate"
          required
        />
      </div>
    </form>
    <table class="table table-striped table-bordered table-responsive-xl">
      <thead>
        <tr class="text-center">
          <th />
          <th />
          <th v-for="h in holes">{{ h }}</th>
          <th>GROSS</th>
          <th>HDCP</th>
          <th>NET</th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr>
          <th />
          <th class="corner">NAME \ PAR</th>
          <td v-for="(par, index) in score.score.par">
            <input class="form-control" type="number" min="1" max="6" required v-model="score.score.par[index]" />
          </td>
        </tr>
        <tr v-for="(s, player_index) in score.score.scores">
          <td>
            <button type="button" class="btn btn-danger" @click="removePlayer(player_index)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
          <td>
            <input
              class="form-control name"
              placeholder="name"
              v-model.trim="s.name"
              required
              :class="{ 'is-invalid': !s.name }"
            />
          </td>
          <td v-for="(ss, hole_index) in s.score">
            <input
              class="form-control score"
              type="number"
              v-model="ss.score"
              min="1"
              max="20"
              required
              @change="dump(player_index, hole_index, ss)"
            />
          </td>
          <td>
            {{ s.gross }}
          </td>
          <td>
            <input
              class="form-control hdcp"
              type="number"
              step="0.1"
              required
              v-model="s.hdcp"
              @change="changeHdcp(player_index)"
            />
          </td>
          <td>
            {{ s.net }}
          </td>
        </tr>
      </tbody>
    </table>
    <div class="form-group row functions ml-1">
      <button type="button" class="btn btn-primary mx-2" @click="addPlayer">
        <i class="bi bi-plus-circle"></i> Add Player
      </button>
      <button type="button" class="btn btn-primary mx-2" @click="sort"><i class="bi bi-sort-down"></i> Sort</button>
      <button type="button" class="btn btn-info mx-2" @click="helpNearpin">Set ニアピンホール</button>
    </div>
    <hr />
    <p>やること：</p>
    <ul>
      <li>がんばって全部打つ</li>
      <ul>
        <li>スコア</li>
        <li>コース名</li>
        <li>日時</li>
      </ul>
      <li>疲れたらとりあえず送信して、後で編集する(NEW)</li>
      <li>Sortを押す</li>
      <li>ニアピン設定する</li>
    </ul>
  </div>
</template>
<style scoped>
table input {
  width: 5em;
}
table input.name {
  width: 100px;
}
table input.hdcp {
  width: 7em;
}

table .corner {
  white-space: nowrap;
}

table input.birdie {
  color: blue;
}
td.nearpin {
  background: green;
}
.functions .btn {
  width: 200px;
}
</style>

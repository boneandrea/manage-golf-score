<script setup>
import { defineEmits, ref, computed } from 'vue'
import { HOLE, getPrize } from '@/utils/utils'
const props = defineProps(['peria_holes'])
const emit = defineEmits(['updateManualData', 'resetManualData', 'setPeriaHoles'])
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const courseInfo = ref({ name: '', date: null })
const par = ref([...Array(HOLE)].map((_, i) => null))
const NEWUSER = {
  name: '',
  score: [...Array(HOLE)].map((_, i) => null),
  gross: 0,
  hdcp: 0,
  net: 0,
}

const score = ref([])
const holes = [...Array(HOLE)].map((_, i) => i + 1)
const changeHdcp = (index) => {
  score.value[index].net = (
    Math.round((score.value[index].gross - parseFloat(score.value[index].hdcp)) * 10) / 10
  ).toFixed(1)
}

const helpNearpin = () => {
  alert('ニアピンはRESULT画面で設定してください')
}

const dump = (player_index, hole_index) => {
  const gross = score.value[player_index].score.reduce(function (sum, element) {
    return sum + element
  }, 0)
  score.value[player_index].gross = gross
  score.value[player_index].net = gross - score.value[player_index].hdcp
}
const sort = () => {
  if (!courseInfo.value.name) {
    alert('入力が完了していません')
    return
  }
  if (!courseInfo.value.date) {
    alert('入力が完了していません')
    return
  }
  score.value.sort((a, b) => a.net - b.net)
  update()
}

const addPlayer = () => {
  score.value.push(structuredClone(NEWUSER))
}
const removePlayer = (index) => {
  const name = score.value[index].name
  if (!confirm(`${name} さんを消しますよ？？？OK?`)) return
  score.value.splice(index, 1)
}
const update = () => {
  emit('updateManualData', score.value, par.value, courseInfo.value)
}

const save = () => {
  if (!confirm('入力内容を保存しますか？')) return
  const data = {
    peria_holes: [...props.peria_holes],
    courseInfo: courseInfo.value,
    par: par.value,
    score: score.value,
  }
  localStorage.setItem('golf-gplus', JSON.stringify(data))
  alert('saved')
}
const restore = () => {
  if (!confirm('保存された内容を読み込みますか？')) return
  try {
    const data = JSON.parse(localStorage.getItem('golf-gplus'))
    courseInfo.value.name = data.courseInfo.name
    courseInfo.value.date = data.courseInfo.date
    score.value.splice(0)
    data.score.forEach((s) => score.value.push(s))
    par.value.splice(0)
    data.par.forEach((p) => par.value.push(p))
    emit('resetManualData')
    emit('setPeriaHoles', data.peria_holes)
  } catch (e) {
    alert('復元失敗... Arrrrggghhhh')
  }
}
addPlayer()
</script>
<template>
  <div>
    <form>
      <div class="form-group row ml-1">
        <input
          class="form-control w-25"
          :class="{ 'is-invalid': courseInfo.name === '' }"
          placeholder="コース名"
          v-model.trim="courseInfo.name"
          required
        />
      </div>
      <div class="form-group row ml-1">
        <input
          class="form-control w-25"
          :class="{ 'is-invalid': courseInfo.date === null }"
          placeholder="日時"
          type="date"
          v-model="courseInfo.date"
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
          <th>NAME \ PAR</th>
          <td v-for="(_p, index) in par">
            <input class="form-control" type="number" min="1" max="6" required v-model="par[index]" />
          </td>
        </tr>
        <tr v-for="(s, player_index) in score">
          <td>
            <button type="button" class="btn btn-danger" @click="removePlayer(player_index)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
          <td>
            <input class="form-control name" placeholder="name" v-model.trim="s.name" required />
          </td>
          <td v-for="(hole, hole_index) in holes">
            <input
              class="form-control score"
              type="number"
              v-model="s['score'][hole_index]"
              min="1"
              max="20"
              required
              @change="dump(player_index, hole_index)"
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
    <div class="form-group row functions ml-1">
      <button type="button" class="btn btn-danger mx-2" @click="save">Save</button>
      <button type="button" class="btn btn-danger mx-2" @click="restore">Restore</button>
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
      <li>疲れたらSave/Restoreもできる</li>
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

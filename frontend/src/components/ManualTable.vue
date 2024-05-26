<script setup>
import { defineEmits, ref, computed } from 'vue'
import { getPrize } from '@/utils/utils'
const emit = defineEmits(['updateManualData'])
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const HOLE = 18
const courseInfo = ref({ name: '', date: null })
const par = ref([4, 4, 5, 3, 4, 5, 4, 3, 4, 4, 4, 4, 5, 3, 4, 5, 3, 4])
const score = ref([
  {
    name: 'AAA',
    score: [9, 8, 9, 3, 8, 6, 6, 5, 7, 9, 6, 8, 9, 2, 7, 7, 5, 9],
    gross: 15,
    hdcp: 0,
    net: 0,
  },
  {
    name: 'BBB',
    score: [2, 2, 2, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    gross: 6,
    hdcp: 0,
    net: 0,
  },
])
const holes = [...Array(HOLE)].map((_, i) => i + 1)
const changeHdcp = (index) => {
  score.value[index].net = (
    Math.round((score.value[index].gross - parseFloat(score.value[index].hdcp)) * 10) / 10
  ).toFixed(1)
}

const helpNearpin = () => {
  alert('ニアピンは下の画面で設定してください')
}

const dump = (player_index, hole_index) => {
  const gross = score.value[player_index].score.reduce(function (sum, element) {
    return sum + element
  }, 0)
  score.value[player_index].gross = gross
  score.value[player_index].net = gross - score.value[player_index].hdcp

  const prize = getPrize(par.value[hole_index], score.value[player_index].score[hole_index])
  if (prize === 'birdie') {
  }
  if (prize === 'B') {
  }
}
const sort = () => {
  score.value.sort((a, b) => a.net - b.net)
  update()
}
/*
    3 holeの場合
    score=[
    [4,5,7],
    [3,4,2],
    ]
  */
const addPlayer = () => {
  score.value.push({
    name: '',
    score: [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    gross: 0,
    hdcp: 0,
    net: 0,
  })
}
const removePlayer = (index) => {
  const name = score.value[index].name
  if (!confirm(`${name} さんを消しますよ？？？OK?`)) return
  score.value.splice(index, 1)
}
const update = () => {
  emit('updateManualData', score.value, par.value, courseInfo.value)
}
</script>
<template>
  <div>
    <form>
      <div class="form-group row ml-1">
        <input class="form-control w-25" placeholder="コース名" v-model="courseInfo.name" required />
      </div>
      <div class="form-group row ml-1">
        <input class="form-control w-25" placeholder="日時" type="date" v-model="courseInfo.date" required />
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
            <button type="button" class="btn btn-danger btn-lg" @click="removePlayer(player_index)">Remove</button>
          </td>
          <td>
            <input class="form-control name" placeholder="name" v-model="s.name" required />
          </td>
          <td v-for="(hole, hole_index) in holes" title="ニアピンにする場合はクリック">
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
      <button type="button" class="btn btn-primary mx-2" @click="addPlayer">Add Player</button>
      <button type="button" class="btn btn-primary mx-2" @click="sort">Sort</button>
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
      <li>Sortを押す</li>
      <li>ニアピン設定する</li>
    </ul>
  </div>
</template>
<style scoped>
td {
  vertical-align: middle !important;
}
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

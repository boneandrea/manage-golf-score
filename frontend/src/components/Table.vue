<script setup>
import { ref, computed } from 'vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const msg = '本日のスコア'
const game = ref({})
const peria_holes = ref(['', '', '', '', '', '', '', '', '', '', '', ''])
const members = ref([])
const spinner0 = ref(false)
const spinner1 = ref(false)
const API_ROOT = import.meta.env.VITE_API_ROOT
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

const scoreByHole = (scores, hole_no) => scores.find((e) => e.hole === hole_no).score
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
function dragList(e, i) {
    console.log(e, i)
    console.log(members.value)
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

function send() {
    console.log(members.value)
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
        })
        .catch((e) => {
            spinner1.value = false
            console.error(e)
            alert(e)
        })
}
const today = new Date()
</script>
<template>
    <div>
        <h1 class="green">スコア編集</h1>
        <p>
            <a href="https://boneandrea.github.io/gplus-golf-score/" target="_blank">ランキングページ</a>
        </p>
        <p>
            <a href="./pdf">download</a>
        </p>
        <h3 class="green">新ペリホール番号</h3>
        <div class="form-group row peria">
            <div v-for="(hole, index) in peria_holes.slice(0, 6)" class="col-sm-2">
                <input
                    class="form-control"
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
        <div class="form-group row peria">
            <div v-for="(hole, index) in peria_holes.slice(6, 12)" class="col-sm-2">
                <input
                    class="form-control"
                    :class="{ 'is-invalid': inValidPeriaHole(peria_holes[index + 6]) }"
                    type="number"
                    v-model="peria_holes[index + 6]"
                    min="1"
                    max="18"
                    required
                />
            </div>
        </div>
        <hr />
        <h3 class="green">データ取得</h3>
        <div class="form-group row">
            <div class="col">
                <input class="form-control" type="url" id="url" placeholder="本日のスコアのURL" autofocus />
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
        <hr />
        <h2 v-if="game.date" class="green">
            {{ game.course }} {{ game.date.getFullYear() }}/{{ game.date.getMonth() + 1 }}/{{ game.date.getDate() }}
        </h2>
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
                        <input
                            class="form-control responsive"
                            type="text"
                            style="min-width: 10em"
                            v-model="member.name"
                        />
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
        <div class="form-group row">
            <div class="col">
                <button class="btn btn-primary" @click="send" :disabled="incompletedPeriaHoles || spinner0 || spinner1">
                    送信
                </button>
            </div>
            <div class="col">
                <div v-show="spinner1" class="spinner-border text-secondary" role="status" />
            </div>
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
@media (min-width: 1024px) {
    .greetings h1,
    .greetings h3 {
        text-align: left;
    }
}
h1 {
    margin-top: 0.5em;
}
</style>

<script setup>
import { ref, computed } from 'vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const HOLE = 18
const nearpin = ref([])
const nearpinPlayer = ref([])
const par = ref([
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
])
const score = ref([
    {
        name: '',
        score: [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
        ],
        gross: 0,
        hdcp: 0,
        net: 0,
    },
])
const holes = [...Array(HOLE)].map((_, i) => i + 1)
const changeHdcp = (index) => {
    score.value[index].net = score.value[index].gross - parseFloat(score.value[index].hdcp)
}
const checkNearpin = (hole, player_index) =>
    nearpinPlayer.value.find((e) => e.player === player_index && e.hole === hole)

const setNearpin = (hole, player_index) => {
     if(event.target.tagName.toUpperCase() !== "TD") return
    if (!nearpin.value.includes(hole)) return
    if (nearpinPlayer.value.find((e) => e.player === player_index && e.hole === hole)) {
        const index = nearpinPlayer.value.findIndex((e) => e.player === player_index && e.hole === hole)
        nearpinPlayer.value.splice(index, 1)
    } else {
        nearpinPlayer.value.push({ player: player_index, hole: hole })
    }
}
const helpNearpin = () => {
    alert('ニアピン対象ホール番号をクリックしてください\nそのあと、スコアの近くをクリックして下さい')
}
 const setNearpinHoleNumber = (hole) => {
    if (nearpin.value.includes(hole)) {
        const index = nearpin.value.findIndex((e) => e === hole)
        nearpin.value.splice(index, 1)
    } else {
        nearpin.value.push(hole)
    }
}
const getPrize = (par, shot) => {
    const diff = par - shot
    if (shot === 1) return 'HOLEINONE'

    switch (diff) {
        case -3:
            return 'TB'
        case -2:
            return 'DB'
        case -1:
            return 'B'
        case 0:
            return 'par'
        case 1:
            return 'birdie'
        case 2:
            return 'eagle'
        case 3:
            return 'ALBATROSS'
        default:
            return null
    }
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
        score: [],
        gross: 0,
        hdcp: 0,
        net: 0,
    })
}
const removePlayer = (index) => {
    if (!confirm('remove OK?')) return
    score.value.splice(index, 1)
}
</script>
<template>
    <div>
        <table class="table table-striped table-bordered table-responsive-xl">
            <thead>
                <tr class="text-center">
                    <th />
                    <th />
                    <th v-for="h in holes" @click="setNearpinHoleNumber(h)">
                        {{ h }}<span v-show="nearpin.includes(h)">[N]</span>
                    </th>
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
                        <button type="button" class="btn btn-danger btn-lg" @click="removePlayer(player_index)">
                            Remove
                        </button>
                    </td>
                    <td>
                        <input class="form-control name" placeholder="name" v-model="s.name" required />
                    </td>
                    <td
                        v-for="(hole, hole_index) in holes"
                        :class="{ nearpin: checkNearpin(hole, player_index) }"
                        @click="setNearpin(hole, player_index)"
                        title="ニアピンにする場合はクリック"
                    >
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
        <div class="form-group row">
            <button type="button" class="btn btn-primary btn-lg mx-2" @click="addPlayer">Add Player</button>
            <button type="button" class="btn btn-primary btn-lg mx-2" @click="sort">Sort</button>
            <button type="button" class="btn btn-primary btn-lg mx-2" @click="helpNearpin">Set ニアピンホール</button>
        </div>

        <hr />
        <p>やること：</p>
        <ul>
            <li>がんばって全部打つ</li>
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
</style>

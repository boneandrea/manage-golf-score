<script setup>
import { ref, computed } from 'vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const HOLE = 18
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
    console.log(prize)
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
                        <button type="button" class="btn btn-danger btn-lg" @click="removePlayer(player_index)">
                            Remove
                        </button>
                    </td>
                    <td>
                        <input class="form-control name" placeholder="name" v-model="s.name" required />
                    </td>
                    <td v-for="(hole, hole_index) in holes">
                        <input
                            class="form-control"
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
</style>

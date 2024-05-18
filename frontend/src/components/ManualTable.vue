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
    },
])
const holes = [...Array(HOLE)].map((_, i) => i + 1)
const dump = () => {
    console.log(par.value)
    console.log(score.value[0].score)
}
/*
   3 holeの場合
   score=[
   [4,5,7],
   [3,4,2],
   ]
 */
const addPlayer = () => {
    score.value.push({ name: '', score: [] })
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
                <tr v-for="(s, index) in score">
                    <td>
                        <button type="button" class="btn btn-danger btn-lg" @click="removePlayer(index)">Remove</button>
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
                            max="18"
                            required
                            @change="dump"
                        />
                    </td>
                    <td>
                        {{ 55 }}
                    </td>
                    <td>
                        <input class="form-control" type="number" min="1" max="18" required />
                    </td>
                    <td>
                        {{ 55 }}
                    </td>
                </tr>
            </tbody>
        </table>
        <button type="button" class="btn btn-primary btn-lg" @click="addPlayer">Add Player</button>
        <hr />
        <p>やること：</p>
        <ul>
            <li>がんばって全部打つ</li>
        </ul>
    </div>
</template>
<style scoped>
table input {
    width: 50px;
}
table input.name {
    width: 100px;
}
</style>

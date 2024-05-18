<script setup>
  import { ref, computed } from 'vue'
  const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
  const NUM_PLAYER=20
  const HOLE=18
  const score=[]
  const players=ref([...Array(NUM_PLAYER)].map((_, i) => i+1))
  const holes=[...Array(HOLE)].map((_, i) => i+1)
  console.log(holes)
  /*
  3 holeの場合
  score=[
      [4,5,7],
  [3,4,2],
  ]
  */
  const addPlayer=()=>{
  players.value.push({})
  }
  const removePlayer=index=>{
  players.value.splice(index,1)
  }
</script>
<template>
  <div>
    <table class="table table-striped table-bordered table-responsive-xl">
      <thead>
        <tr class="text-center">
          <th/>
          <th v-for="h in holes" >{{h}}</th>
          <th>GROSS</th>
          <th>HDCP</th>
          <th>NET</th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr>
          <th/>
          <th>NAME \ PAR</th>
          <td v-for="(hole,index) in holes">
            <input
              class="form-control"
              type="number"
              min="1"
              max="6"
              required
              />
          </td>
        </tr>
        <tr v-for="(player,index) in players">
          <td>
            <button type="button" class="btn btn-danger btn-lg" @click="removePlayer(index)">X</button>
          </td>
          <td>
            <input
              class="form-control name"
              placeholder="name"
              required
              />
          </td>
          <td v-for="(hole,index) in holes">
            <input
              class="form-control"
              type="number"
              min="1"
              max="18"
              required
              />
          </td>
          <td>
            {{55}}
          </td>
          <td>
            <input
              class="form-control"
              type="number"
              min="1"
              max="18"
              required
              />
          </td>
          <td>
            {{55}}
          </td>
        </tr>
      </tbody>
    </table>
    <button type="button" class="btn btn-primary btn-lg" @click="addPlayer">Add Player</button>
    <p>やること：</p>
    <ul>
      <li>がんばって全部打つ</li>
    </ul>
  </div>
</template>
<style scoped>
  table input{
  width: 50px
  }
  table input.name{
  width: 100px
  }
</style>

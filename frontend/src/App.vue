<script setup>
import { ref, computed } from 'vue'
import Sidebar from './components/Sidebar.vue'
import { RouterView } from 'vue-router'

const data = ref({})
const recv = (e) => {
  Object.keys(data.value).forEach((k) => delete data.value[k])
  data.value = Object.assign(data.value, e)
}
</script>

<template>
  <Sidebar @receive="recv" />
  <RouterView :data="data" />
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>

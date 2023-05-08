<template>
  <div id="app">
    <STGAN />
  </div>
</template>

<script>
import STGAN from './components/STGAN.vue'

export default {
  name: 'App',
  components: {
    STGAN
  }
}
</script>

<style>
html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>

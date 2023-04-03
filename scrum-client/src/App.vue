<script>
import LoginRegisterPage from './components/LoginRegisterPage.vue'
import MainPage from './components/MainPage.vue'
import { useMainStore } from '@/stores/main'


export default {
  setup() {
      const store = useMainStore()
      return { store }
  },
  components: {
    LoginRegisterPage,
    MainPage,
  }
}
</script>

<template>
  <MainPage v-if="this.store.username" />
  <LoginRegisterPage v-else/>
</template>

<style>
  #app {
    width: 100vw;
    height: 100vh;
    background-color: rgb(229, 249, 210);
  }
  .dropdown {
    background-color: rgb(232, 232, 170);
    border-radius: 4px;
  }
  .btn {
    background-color: rgb(232, 232, 170);
    border-radius: 4px;
    padding: 6px;
  }
  .btn:hover {
    background-color: rgb(145, 150, 107);
  }
</style>
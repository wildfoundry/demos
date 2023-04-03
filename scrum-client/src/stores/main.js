import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    baseAPIURL: 'http://localhost:8000/', // or https://your-url-1234.dataplicity.io/',
    username: '',
    password: '',
  })
})

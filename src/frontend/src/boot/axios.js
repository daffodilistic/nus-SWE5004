// src/boot/axios.js

import { boot } from 'quasar/wrappers'
import axios from 'axios'

const serverUrl =
process.env.NODE_ENV === "production"
  ? "YOUR_PRODUCTION_SERVER_URL"
  : "https://api.mariotoilet.xyz/v1";
const api = axios.create({ baseURL: serverUrl })

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { axios, api }
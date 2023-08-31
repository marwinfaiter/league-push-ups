import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from "axios"
import App from "./App.vue"
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

const app = createApp(App)

class BackendClient {
    constructor() {
        this.base_url = "http://localhost:5000"
    }
    async get(url) {
        return await axios({
            method: "get",
            url: `${this.base_url}/${url}`,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            withCredentials: true,
        })
    }
    async post(url, data) {
        return await axios({
            method: "post",
            url: `${this.base_url}/${url}`,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data: data,
            withCredentials: true,
        })
    }
    async delete(url, data) {
        return await axios({
            method: "delete",
            url: `${this.base_url}/${url}`,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data: data,
            withCredentials: true,
        })
    }
    async login(username, password) {
        return this.post("login", {username, password})
    }
    async logout() {
        return this.post("logout")
    }
}

app.config.globalProperties.backend_client = new BackendClient()

const router = createRouter({
    history: createWebHistory(),
    routes: App.data().routes
})

const store = new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })],
    state: {
        username: null
    },
    mutations: {
        set_login(state, username) {
            state.username = username
        }
    }
});

app.config.globalProperties.store = store

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      if (!store.state.username) {
        next("/")
      } else {
        next() // go to wherever I'm going
      }
    } else {
      next() // does not require auth, make sure to always call next()!
    }
  })

app.use(router)
app.use(Vuex);
app.mount('#app')

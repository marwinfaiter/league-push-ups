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
        return await axios
            .get(`${this.base_url}/${url}`)
    }
    async post(url, data) {
        return await axios
            .post(`${this.base_url}/${url}`, data)
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

app.config.globalProperties.store = new Vuex.Store({
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

app.use(router)
app.use(Vuex);
app.mount('#app')

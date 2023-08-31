import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from "axios"
import App from "./App.vue"

const app = createApp(App)

class BackendClient {
    constructor() {
        this.base_url = "http://localhost:5000"
    }
    async get(url) {
        console.log(`Querying ${this.base_url}/${url}`);
        return await axios
            .get(`${this.base_url}/${url}`)
            .then(response => {
                return response.data;
            });
    }
}

app.config.globalProperties.backend_client = new BackendClient()

const router = createRouter({
    history: createWebHistory(),
    routes: App.data().routes
})

app.use(router)
app.mount('#app')

import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from "./App.vue"
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { fas } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(fas)

import BackendClient from './javascript/backend_client';

const app = createApp(App)

const router = createRouter({
    history: createWebHashHistory(),
    routes: App.data().routes
})

const store = new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })],
    state: {
        login: null
    },
    mutations: {
        set_login(state, login_data) {
            state.login = login_data
        }
    }
});

app.config.globalProperties.backend_client = new BackendClient(store)

app.config.globalProperties.store = store

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      if (!store.state.login) {
        next("/")
      } else {
        next() // go to wherever I'm going
      }
    } else {
      next() // does not require auth, make sure to always call next()!
    }
  })

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(VueSweetalert2)
app.mount('#app')

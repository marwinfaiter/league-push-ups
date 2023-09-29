import axios from "axios"
import Swal from 'sweetalert2'

export default class BackendClient {
    constructor(store) {
        this.base_url = process.env.VUE_APP_BACKEND_URL;
        this.store = store;
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
        }).catch(error => {
            if (error.response.status == 401) {
                this.store.commit("set_login", false)
            }
            if (error.response) {
                new Swal({
                    text: error.response.data.message ? error.response.data.message : error.response.data,
                    icon: "error",
                });
            }
        });
    }
    async post(url, data={}) {
        return await axios({
            method: "post",
            url: `${this.base_url}/${url}`,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data: data,
            withCredentials: true,
        }).catch(error => {
            if (error.response.status == 401) {
                this.store.commit("set_login", false)
            }
            if (error.response) {
                new Swal({
                    text: error.response.data.message ? error.response.data.message : error.response.data,
                    icon: "error",
                });
            }
        });
    }
    async delete(url, data={}) {
        return await axios({
            method: "delete",
            url: `${this.base_url}/${url}`,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data: data,
            withCredentials: true,
        }).catch(error => {
            if (error.response) {
                new Swal({
                    text: error.response.data,
                    icon: "error",
                });
            }
        });
    }
    async login(username, password) {
        return this.post("login", {username, password})
        .then(response => {
            console.log(response)
            if (response) {
                this.store.commit("set_login", response.data);
                return response;
            }
        })
    }
    async logout() {
        return this.post("logout")
        .then(response => {
            this.store.commit("set_login", null);
            return response;
        })
    }
    async toggle_player_pushups_finished(match_player_id) {
        return this.post(`match_player/${match_player_id}/toggle_pushups_finished`)
    }
}

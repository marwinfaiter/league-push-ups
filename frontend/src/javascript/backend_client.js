import axios from "axios"
import Swal from 'sweetalert2'

export default class BackendClient {
    constructor() {
        this.base_url = "/api"
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
            if (error.response) {
                new Swal({
                    text: error.response.data,
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
            if (error.response) {
                new Swal({
                    text: error.response.data,
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
    }
    async logout() {
        return this.post("logout")
    }
    async toggle_player_pushups_finished(match_player_id) {
        return this.post(`match_player/${match_player_id}/toggle_pushups_finished`)
    }
}

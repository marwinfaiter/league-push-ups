<template>
  <div class="container">
    <div class="row">
      <div class="col-md-5"></div>
      <div class="col-md-2">
        <select v-model="current_user" class="form-select">
          <option v-for="username in Object.keys(this.user_settings)" :value="username" :key="username">{{ username }}</option>
        </select>
      </div>
      <div class="col-md-5"></div>
    </div>

    <template v-if="this.user_settings[this.current_user]">
      <div class="row">
        <div class="col">
          <table class="table table-sm table-hover rounded" style="overflow: hidden">
            <thead class="table-secondary">
              <tr>
                <th>Active</th>
                <th>Minimum Push Ups</th>
                <th>Maximum Push Ups</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <div class="form-check form-switch">
                    <label class="form-check-label" for="active_switch">
                      <input class="form-check-input" role="switch" type="checkbox" id="active_switch" v-model="this.user_settings[this.current_user].settings.active"/>
                    </label>
                  </div>
                </td>
                <td><input v-model="this.user_settings[this.current_user].settings.minimum_push_ups"/></td>
                <td><input v-model="this.user_settings[this.current_user].settings.maximum_push_ups"/></td>
                <td><button type="button" @click="update_settings(this.current_user)" class="btn btn-sm btn-info">Update</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <table class="table table-sm table-hover rounded" style="overflow: hidden">
            <thead class="table-light">
              <tr>
                <th>Summoners</th>
                <th><button data-bs-toggle="modal" data-bs-target="#new_summoner_modal" class="btn btn-sm btn-primary">Add</button></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="summoner of this.user_settings[this.current_user].summoners" :key="summoner.id">
                <td>{{ summoner.name }}</td>
                <td><button type="button" @click="delete_summoner(summoner.name)" class="btn btn-sm btn-danger">Delete</button></td>
              </tr>
            </tbody>
          </table>
          <div class="modal" id="new_summoner_modal">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-body">
                    <label for="newSummonerName" class="form-label">Summoner name</label>
                    <input v-model="this.new_summoner" type="text" class="form-control" id="newSummonerName" aria-describedby="summonerHelp">
                    <div id="summonerHelp" class="form-text">Needs to be unique and is case sensitive</div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  <button @click="add_summoner" type="button" class="btn btn-primary">Save changes</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <table class="table table-sm table-hover rounded" style="overflow: hidden">
            <thead class="table-light">
              <tr>
                <th>API Keys</th>
                <th><button @click="create_api_key" class="btn btn-sm btn-primary">Create</button></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="api_key of this.user_settings[this.current_user].api_keys" :key="api_key.id">
                <td>{{ api_key.value }}</td>
                <td><button type="button" @click="delete_api_key(api_key.value)" class="btn btn-sm btn-danger">Delete</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
    name: 'UserSettingsView',
    data() {
      return {
        user_settings: {},
        current_user: this.store.state.login.username,
        new_summoner: null
      };
    },
    async created() {
      await this.getData();
    },
    methods: {
      async getData() {
        if (this.store.state.login.groups.includes("leaguepushups-admins")) {
          this.user_settings = await this.backend_client.get(`user`).then(response => response.data);
        }
        else {
          this.user_settings = await this.backend_client.get(`user/${this.current_user}`).then(response => response.data);
        }
      },
      async update_settings(username) {
        await this.backend_client.post(`user/${username}`, this.user_settings[this.current_user].settings).then(response => {
          if (response) {
              this.$router.go();
              return response;
            }
        })
      },

      async create_api_key() {
        await this.backend_client.post(`user/${this.current_user}/api_keys`);
        this.$router.go()
      },
      async delete_api_key(api_key) {
        await this.backend_client.delete(`user/${this.current_user}/api_keys`, api_key)
        this.$router.go()
      },

      async add_summoner() {
        await this.backend_client.post(`user/${this.current_user}/summoners`, this.new_summoner).then(response => {
            if (response) {
              this.$router.go();
              return response;
            }
        });
      },
      async delete_summoner(summoner) {
        await this.backend_client.delete(`user/${this.current_user}/summoners`, summoner).then(response => {
          if (response) {
              this.$router.go();
              return response;
            }
        })
      }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>

<template>
  <div class="container">
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
                <input class="form-check-input" role="switch" type="checkbox" id="active_switch" v-model="active"/>
              </label>
            </div>
          </td>
          <td><input v-model="minimum_push_ups"/></td>
          <td><input v-model="maximum_push_ups"/></td>
          <td><button type="button" @click="update_settings()" class="btn btn-sm btn-danger">Update</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
    name: 'UserSettingsView',
    data() {
      return {
        minimum_push_ups: null,
        maximum_push_ups: null,
        active: null
      };
    },
    async created() {
      await this.getData();
    },
    methods: {
      async getData() {
        let data = await this.backend_client.get(`user`).then(response => response.data);
        this.minimum_push_ups = data.minimum_push_ups;
        this.maximum_push_ups = data.maximum_push_ups;
        this.active = data.active;
      },
      async update_settings() {
        await this.backend_client.post(`user`, {active: this.active, minimum_push_ups: this.minimum_push_ups, maximum_push_ups: this.maximum_push_ups}).then(response => {
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

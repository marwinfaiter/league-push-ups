<template>
  <div class="container">
    <table class="table table-sm table-hover rounded" style="overflow: hidden">
      <thead class="table-light">
        <tr>
          <th>Reward</th>
          <th>Description</th>
          <th>Push Ups</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reward in this.rewards" :key="reward.id">
          <td><input :ref="`${reward.id}_name`" :placeholder="reward.name"/></td>
          <td><input :ref="`${reward.id}_description`" :placeholder="reward.description"/></td>
          <td><input :ref="`${reward.id}_push_ups`" :placeholder="reward.push_ups"/></td>
          <td><button type="button" @click="update_reward(reward.id)" class="btn btn-info">Update</button></td>
          <td><button type="button" @click="delete_reward(reward.id)" class="btn btn-danger">Delete</button></td>
        </tr>
        <tr>
          <td><input v-model="new_reward" placeholder="Name"></td>
          <td><input v-model="new_reward_description" placeholder="Description"></td>
          <td><input v-model="new_reward_push_ups" placeholder="Push Ups"></td>
          <td></td>
          <td><button @click="add_reward" class="btn btn-primary">Add</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
    name: 'RewardsView',
    data() {
      return {
        rewards: [],
        new_reward: null,
        new_reward_description: null,
        new_reward_push_ups: null,
      };
    },
    async created() {
      await this.getData();
    },
    methods: {
      async getData() {
        this.rewards = await this.backend_client
          .get("rewards")
          .then(
            response => response.data
          );
      },
      async add_reward() {
        if (!this.new_reward || !this.new_reward_push_ups) {
          return this.$swal({
            title: "Missing Reward or Push Ups",
            icon: "error",
          });
        }
        await this.backend_client.post("rewards", {name: this.new_reward, description: this.new_reward_description, push_ups: this.new_reward_push_ups}).then(response => {
            if (response) {
              this.$router.go();
              return response;
            }
        });
      },
      async update_reward(reward_id) {
        let updated_name = this.$refs[`${reward_id}_name`][0].value;
        let updated_description = this.$refs[`${reward_id}_description`][0].value;
        let updated_push_ups = this.$refs[`${reward_id}_push_ups`][0].value;

        await this.backend_client.post(`rewards/${reward_id}`, {name: updated_name, description: updated_description, push_ups: updated_push_ups}).then(response => {
          if (response) {
              this.$router.go();
              return response;
            }
        })
      },
      async delete_reward(reward_id) {
        await this.backend_client.delete(`rewards/${reward_id}`).then(response => {
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

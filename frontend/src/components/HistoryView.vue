<template>
    <div v-for="match in this.matches" :key="match.id" class="container">
      <table class="table table-sm table-hover rounded" style="overflow: hidden">
        <thead role="button" data-bs-toggle="modal" :data-bs-target="'#match_modal_'+ match.id" class="table-light">
          <tr>
            <th>Summoner Name</th>
            <th>Kills</th>
            <th>Deaths</th>
            <th>Assists</th>
            <th>KDA</th>
            <th>Kill Participation</th>
            <th>Push Ups</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="player in match.players" :key="player.id">
            <td>{{ player.SummonerName }}</td>
            <td class="text-success">{{ player.Kills }}</td>
            <td class="text-danger">{{ player.Deaths }}</td>
            <td class="text-warning">{{ player.Assists }}</td>
            <td>{{ format_number(player.kda) }}</td>
            <td>{{ format_number(player.kill_participation * 100) }}%</td>
            <td class="text-info">{{ player.push_ups }}
              <font-awesome-icon v-if="player.PushUpsFinished" role="button" @click="toggle_player_pushups_finished(player)" :icon="['fas', 'check']" style="color: #2ff109;" />
              <font-awesome-icon v-else role="button" @click="toggle_player_pushups_finished(player)" :icon="['fas', 'ban']" style="color: #ff0000;" />
            </td>
          </tr>
        </tbody>
      </table>
      <div class="modal" :id="'match_modal_' + match.id">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <table class="table table-borderless table-sm table-hover rounded" style="overflow: hidden; margin: 0">
              <thead class="table-light">
                <tr>
                  <th>Session ID</th>
                  <th>Session Start</th>
                  <th>Game ID</th>
                  <th>Game Start</th>
                  <th>Team Kills</th>
                  <th>Minimum Push Ups</th>
                  <th>Maximum Push Ups</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ match.Session.id }}</td>
                  <td>{{ match.Session.date_time }}</td>
                  <td>{{ match.MatchID }}</td>
                  <td>{{ match.date_time }}</td>
                  <td>{{ match.TeamKills }}</td>
                  <td>{{ match.MinPushUps }}</td>
                  <td>{{ match.MaxPushUps }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
    name: 'HistoryView',
    data() {
        return {
            matches: []
        };
    },
    async created() {
        await this.getData();
    },
    methods: {
        async getData() {
            this.matches = await this.backend_client
              .get("matches")
              .then(response => response.data.reverse());
        },
        format_number(number) {
          return parseFloat(number).toFixed(2)
        },
        check_allowed_to_edit(player) {
          if (this.store.state.login.groups.includes("leaguepushups-admins")) {
            return true;
          }
          if (this.store.state.login.summoners.includes(player.SummonerName)) {
            return true;
          }
          return false;
        },
        toggle_player_pushups_finished(player) {
          if (!this.store.state.login) {
            return this.$swal({
              title: "You are not logged in",
              icon: "error",
            });
          }
          if (!this.check_allowed_to_edit(player)) {
            return this.$swal({
              title: "You cannot edit someone elses match",
              icon: "error",
            });
          }

          if (!this.store.state.login.groups.includes("leaguepushups-admins") && !player.PushUpsFinished) {
            return this.$swal({
                title: "You are not allowed to mark as done again",
                icon: "warning",
            });
          }

          return this.$swal({
            title: `Mark push ups as ${player.PushUpsFinished ? "undone": "done"}?`,
            text: "Are you sure? You won't be able to revert this!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Yes, go ahead!"
          }).then((result) => {
            if (result.value) {
              this.backend_client.toggle_player_pushups_finished(player.id)
              .then((response) => {
                if (response) {
                  this.$router.go();
                }
                return response;
              })
            }
          });
        }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>

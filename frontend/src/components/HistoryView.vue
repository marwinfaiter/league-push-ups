<template>
    <nav>
      <ul class="pagination justify-content-center">
        <li :class="{'page-item': true, 'disabled': this.current_page==0}">
          <a @click="this.current_page--" role="button" class="page-link" tabindex="-1">Previous</a>
        </li>
        <li @click="this.current_page=page" :class="{'page-item': true, 'page-link': true, active: page == this.current_page}" role="button" v-for="(n, page) in Math.ceil(this.matches.length / 8)" :key="page">{{ n }}</li>
        <li :class="{'page-item': true, 'disabled': this.current_page==parseInt(this.matches.length / 8)}">
          <a @click="this.current_page++" role="button" class="page-link">Next</a>
        </li>
      </ul>
    </nav>
    <div v-for="match in this.matches.slice(this.current_page * 8, this.current_page * 8 + 8)" :key="match.id" class="container">
      <table class="table table-sm table-hover rounded" style="overflow: hidden">
        <thead role="button" data-bs-toggle="modal" :data-bs-target="'#match_modal_'+ match.id" class="table-light">
          <tr>
            <th>Summoner Name</th>
            <th>Kills</th>
            <th>Deaths</th>
            <th>Assists</th>
            <th>KDA</th>
            <th>Kill Participation</th>
            <th>Minimum Push Ups</th>
            <th>Maximum Push Ups</th>
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
            <td>{{ player.MinPushUps }}</td>
            <td>{{ player.MaxPushUps }}</td>
            <td class="text-info">{{ player.push_ups }}
              <font-awesome-icon v-if="player.Active" role="button" @click="toggle_player_pushups_finished(player)" :icon="['fas', 'check']" style="color: #2ff109;" />
              <font-awesome-icon v-else role="button" @click="toggle_player_pushups_finished(player)" :icon="['fas', 'ban']" style="color: #ff0000;" />
            </td>
          </tr>
        </tbody>
      </table>
      <div class="modal" :id="'match_modal_' + match.id">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-body">
              <table class="table table-borderless table-sm table-hover rounded" style="overflow: hidden; margin: 0">
                <thead class="table-light">
                  <tr>
                    <th>Session ID</th>
                    <th>Session Start</th>
                    <th>Game ID</th>
                    <th>Game Start</th>
                    <th>Team Kills</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ match.Session.id }}</td>
                    <td>{{ match.Session.date_time }}</td>
                    <td>{{ match.MatchID }}</td>
                    <td>{{ match.date_time }}</td>
                    <td>{{ match.TeamKills }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import format_number from '@/javascript/functions';

export default {
    name: 'HistoryView',
    data() {
        return {
            matches: [],
            current_page: 0,
        };
    },
    async created() {
        await this.getData();
    },
    methods: {
        format_number,
        async getData() {
            this.matches = await this.backend_client
              .get("matches")
              .then(response => response.data.reverse());
              for (let page in parseInt(this.matches.length / 8)) {
                console.log(page)
              }
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

          if (!this.store.state.login.groups.includes("leaguepushups-admins") && !player.Active) {
            return this.$swal({
                title: "You are not allowed to mark as done again",
                icon: "warning",
            });
          }

          return this.$swal({
            title: `Mark push ups as ${player.Active ? "undone": "done"}?`,
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

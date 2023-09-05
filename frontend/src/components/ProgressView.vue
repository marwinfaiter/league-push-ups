<template>
    <input class="btn-check" type="radio" name="inlineRadioOptions" id="YEAR" value="group_by_year" v-model="this.current_grouping_method">
    <label class="btn btn-outline-success hover" for="YEAR">YEAR</label>

    <input class="btn-check" type="radio" name="inlineRadioOptions" id="MONTH" value="group_by_month" v-model="this.current_grouping_method">
    <label class="btn btn-outline-success" for="MONTH">MONTH</label>

    <input class="btn-check" type="radio" name="inlineRadioOptions" id="DAY" value="group_by_day" v-model="this.current_grouping_method">
    <label class="btn btn-outline-success" for="DAY">DAY</label>

    <input class="btn-check" type="radio" name="inlineRadioOptions" id="MATCH" value="group_by_match" v-model="this.current_grouping_method" >
    <label class="btn btn-outline-success" for="MATCH">MATCH</label>

    <input class="btn-check" type="radio" name="inlineRadioOptions" id="SESSION" value="group_by_session" v-model="this.current_grouping_method">
    <label class="btn btn-outline-success" for="SESSION">SESSION</label>

  <div v-for="username in Object.keys(this.user_match_groupers)" :key="username" class="container">
    <table class="table table-sm table-hover rounded" style="overflow: hidden">
      <thead class="table-light">
        <tr>
          <th>Username</th>
          <th>Kills</th>
          <th>Deaths</th>
          <th>Assists</th>
          <th>AVG. KDA</th>
          <th>AVG. Kill Participation</th>
          <th>Push Ups</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ username }}</td>
          <td class="text-success">{{ this.user_match_groupers[username].kills }} ({{ format_number(this.user_match_groupers[username].avg_kills) }})</td>
          <td class="text-danger">{{ this.user_match_groupers[username].deaths }} ({{ format_number(this.user_match_groupers[username].avg_deaths) }})</td>
          <td class="text-warning">{{ this.user_match_groupers[username].assists }} ({{ format_number(this.user_match_groupers[username].avg_assists) }})</td>
          <td class="text-secondary">{{ format_number(this.user_match_groupers[username].avg_kda) }}</td>
          <td class="text-secondary">{{ format_number(this.user_match_groupers[username].avg_kill_participation) }}</td>
          <td class="text-info">{{ this.user_match_groupers[username].push_ups }} ({{ format_number(this.user_match_groupers[username].avg_push_ups) }})</td>
        </tr>
        <tr>
          <td colspan="7">
            <div class="progress">
              <div :class="'progress-bar ' + this.colors[index % this.colors.length] " role="progressbar" v-for="(match, index) in group(username)" :key="match.identifier" :style="{width: match.push_ups * 100 / this.user_match_groupers[username].push_ups +'%'}" :aria-valuenow="match.push_ups * 100 / this.user_match_groupers[username].push_ups" aria-valuemin="0" aria-valuemax="100">{{ match.push_ups }} ({{ match.identifier }})</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import MatchGrouper from "../javascript/match_grouper"

export default {
    name: 'ProgressView',
    data() {
        return {
            user_match_groupers: {},
            current_grouping_method: "group_by_match",
            colors: [
              "bg-primary",
              "bg-secondary",
              "bg-success",
              "bg-danger",
              "bg-warning",
              "bg-info",
              "bg-dark",
              "bg-muted",
            ]
        };
    },
    async created() {
        await this.getData();
    },
    methods: {
        async getData() {
            await this.backend_client
              .post("progress")
              .then(response => {
                for (const [username, matches] of Object.entries(response.data)) {
                  this.user_match_groupers[username] = new MatchGrouper(username, matches);
                }
              });

        },
        group(username) {
          return MatchGrouper[this.current_grouping_method](this.user_match_groupers[username].matches)
        },
        format_number(number) {
          return parseFloat(number).toFixed(2)
        }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.btn-outline-success {
  background-color: #198754bb;
  color: #000;
  --bs-btn-active-color: #000;
  --bs-btn-active-bg: #5ed310;
}
  .btn-outline-success:hover, .btn-outline-success:focus, .btn-outline-success:active {
    background-color: #5ed310 !important;
    color: #000;
  }
</style>

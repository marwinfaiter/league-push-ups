<template>
  <div class="container">
    <div class="row" style="margin-bottom: 10px">
      <div class="p-4 shadow-4 rounded-3" style="background-color: hsl(0, 0%, 94%);">
        <h3>
          Hello everyone :)
        </h3>
        This is where we punish ourselves for being bad at League of Legends
        <p>Follow these steps to get started</p>
        <hr class="my-4" />
        <ol style="text-align: left; margin-left:auto;margin-right: auto; width:80%">
          <li>
            Download and install python from <a target="_blank" href="https://www.python.org/downloads/">here</a>
            <ul>
              <li>Right now only python3.11 is tested</li>
            </ul>
          </li>
          <li>Install/Upgrade League Push Ups package
            <ul>
              <li>python3.11 -m pip install -i https://nexus.buddaphest.se/repository/pypi/simple -U league_push_ups</li>
            </ul>
          </li>
          <li>Create an API key after logging in with your username and password</li>
          <li>Run program with python3.11 -m league_push_ups --username {username} --password {API key}</li>
        </ol>
        <img style="border-radius: 5000px; margin: 0px" src="~@/assets/LPU.png">
      </div>
    </div>
    <div class="row">
      <div class="card">
        <div class="card-header">Calculate push ups</div>
        <div class="card-body">
          <table class="table table-sm table-hover rounded">
            <thead>
              <tr>
                <th>Minimum Push Ups</th>
                <th>Maximum Push Ups</th>
                <th>Kills</th>
                <th>Deaths</th>
                <th>Assists</th>
                <th>Team Kills</th>
                <th>KDA</th>
                <th>Kill Participation</th>
                <th>Push Ups</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><input v-model.number="min_push_ups" type="range"/> {{ min_push_ups }}</td>
                <td><input v-model.number="max_push_ups" type="range"/> {{ max_push_ups }}</td>
                <td><input v-model.number="kills" type="range"/> {{ kills }}</td>
                <td><input v-model.number="deaths" type="range"/> {{ deaths }}</td>
                <td><input v-model.number="assists" type="range"/> {{ assists }}</td>
                <td><input v-model.number="team_kills" type="range" min="0" max="200"/> {{ team_kills }}</td>
                <td>{{ this.format_number(this.kda) }}</td>
                <td>{{ this.format_number(this.kill_participation * 100) }}%</td>
                <td>{{ this.format_number(this.push_ups) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import format_number from '@/javascript/functions';

export default {
    name: 'HomePageView',
    data() {
      return {
        min_push_ups: 10,
        max_push_ups: 50,
        kills: 0,
        deaths: 0,
        assists: 0,
        team_kills: 0,
      }
    },
    methods: {
      format_number,
    },
    computed: {
      push_ups() {
        if (this.kda == 0 || this.kill_participation == 0) {
          return this.max_push_ups
        }

        return Math.round(
          Math.min(
            this.max_push_ups,
            this.min_push_ups + (
              (this.max_push_ups / 2) /
              (this.kda * this.kill_participation)
            )
          )
        )
      },
      kda() {
        if (this.deaths == 0) {
          return this.kills + this.assists
        }
        return (this.kills + this.assists) / this.deaths
      },
      kill_participation() {
        if (this.team_kills == 0) {
          return 1
        }
        return (this.kills + this.assists) / this.team_kills
      }
    }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>

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

  <div v-for="username in Object.keys(this.user_match_groupers)" :key="username" class="container-fluid">
    <table class="table table-sm table-hover rounded" style="overflow: hidden; table-layout: fixed;">
      <thead class="table-secondary">
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
            <div class="progress" style="height: 40px">
              <template v-for="(match, index) in group(username)" :key="match.identifier">
                  <div :class="'progress-bar ' + this.colors[index % this.colors.length] " role="progressbar" :style="{width: match.push_ups * 100 / this.user_match_groupers[username].push_ups +'%'}" :aria-valuenow="match.push_ups * 100 / this.user_match_groupers[username].push_ups" aria-valuemin="0" aria-valuemax="100"><span class="fw-bolder">{{ match.push_ups }}</span> <span class="fw-light">({{ match.identifier }})</span></div>
              </template>
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="7">
            <div class="progress">
              <div v-for="reward in this.rewards" :key="reward.id" :class="get_reward_classes(username, reward)" :style="get_reward_styles(reward)" role="button" data-bs-toggle="modal" :data-bs-target="`#reward_modal_${reward.id}`">
                <div>
                  <font-awesome-icon v-if="reward.name.split(',')[0] == 'fas'" :icon="reward.name.split(',')" size="xl"/>
                  <template v-else>{{ reward.name }}</template>
                </div>
              </div>
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" :style="{width: this.user_match_groupers[username].push_ups * 100 / this.rewards.slice(-1)[0]?.push_ups +'%'}" :aria-valuenow="this.user_match_groupers[username].push_ups * 100 / this.rewards.slice(-1)[0]?.push_ups" aria-valuemin="0" aria-valuemax="100">{{ this.user_match_groupers[username].push_ups }}</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-for="reward in this.rewards" :key="reward.id" class="modal" :id="`reward_modal_${reward.id}`">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <table class="table table-borderless table-sm table-hover rounded" style="overflow: hidden; margin: 0">
          <thead class="table-secondary">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Push Ups</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <font-awesome-icon v-if="reward.name.split(',')[0] == 'fas'" :icon="reward.name.split(',')" size="xl"/>
                <template v-else>{{ reward.name }}</template>
              </td>
              <td>{{ reward.description }}</td>
              <td>{{ reward.push_ups }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
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
            ],
            rewards: []
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
            await this.backend_client.get("rewards").then((response) => {
                if (response) {
                    this.rewards = response.data;
                }
            });
        },
        group(username) {
            return MatchGrouper[this.current_grouping_method](this.user_match_groupers[username].matches);
        },
        format_number(number) {
            return parseFloat(number).toFixed(2);
        },
        get_reward_classes(username, reward) {
            let reward_collected = this.user_match_groupers[username]?.push_ups >= reward.push_ups;
            return {
                reward: true,
                "bg-success": reward_collected,
                "bg-warning": !reward_collected,
            };
        },
        get_reward_styles(reward) {
          let left = reward.push_ups * 100 / this.rewards.slice(-1)[0].push_ups;
          if (this.rewards.indexOf(reward) == this.rewards.length - 1) {
            left = 97;
          }
          return {
              left: left + "%",
          };
        },
    },
    components: { FontAwesomeIcon }
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

  .reward {
    position:absolute;
    margin-top:-10px;
    z-index:1;
    opacity: 0.8;
    height:40px;
    width:40px;
    border-radius:25px;

    div {
      margin: auto;
      width: 85%;
      padding: 10px;
    }
  }
</style>

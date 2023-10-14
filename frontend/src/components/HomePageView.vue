<template>
  <div class="container">
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
</template>

<script>
export default {
    name: 'HomePageView',
    data() {
      return {}
    },
    methods: {},
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>

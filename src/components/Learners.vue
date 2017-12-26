<template>
  <div class="wrapper">
    <h2>All Learners</h2>

    <ul>
      <li v-for="learner in learners">
        <router-link :to="{ name: 'Learner', params: { id: learner.id } }">
          {{ learner_identifier(learner) }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    data () {
      return { 'learners': [
        { 'name': '',
          'id': 0,
          'slack_name': '',
          'email': '',
          'goal': ''}] }
    },
    methods: {
      learner_identifier (learner) {
        return learner.name || 'anonymous'
      }
    },
    mounted () {
      fetch('http://localhost:6060/api/learners')
        .then((resp) => resp.json())
        .then((json) => { this.learners = json })
    }
  }
</script>

<style>
div.wrapper { width: 90%;
              max-width: 550px;
              margin: 0 auto }
</style>

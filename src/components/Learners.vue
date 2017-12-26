<template>
  <div>
    <h2>All Learners</h2>

    <ul>
      <li v-for="learner in learners">
        <a :href="learner_url(learner)">{{ learner_identifier(learner) }}</a>
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
      learner_url (learner) {
        return `${learner.id}`
      },
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
div { width: 550px;
      align-self: center }
</style>

<template>
  <div>
    <h2>Learner Profile: {{ learner_identifier }}</h2>

    <dl>
      <dt>Name</dt><dd>{{ learner.name }}</dd>
      <dt>Slack name</dt><dd>{{ learner.slack_name }}</dd>
      <dt>Goal</dt><dd>{{ learner.goal }}</dd>
    </dl>
  </div>
</template>

<script>
export default {
  data () {
    return { 'learner': {
      'name': '',
      'id': 0,
      'email': '',
      'slack_name': '',
      'goal': '' } }
  },
  computed: {
    learner_identifier () {
      return this.learner.name || 'anonymous'
    }
  },
  mounted () {
    const id = this.$route.params.id
    fetch(`http://localhost:6060/api/learners/${id}`)
      .then((resp) => resp.json())
      .then((json) => { this.learner = json })
  }
}
</script>

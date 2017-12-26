<template>
  <div class="wrapper">
    <h2>Learner Profile: {{ learner_identifier }}</h2>

    <transition name="fade">
      <dl v-if="loaded">
        <div><dt>Name</dt><dd>{{ learner.name }}</dd></div>
        <div><dt>Slack name</dt><dd>{{ learner.slack_name }}</dd></div>
        <div><dt>Goal</dt><dd>{{ learner.goal }}</dd></div>
      </dl>
    </transition>
  </div>
</template>

<script>
export default {
  data () {
    return {
      'learner': {
        'name': '',
        'id': 0,
        'email': '',
        'slack_name': '',
        'goal': '' },
      'loaded': false }
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
      .then((json) => {
        this.learner = json
        this.loaded = true
      })
  }
}
</script>

<style>
div.wrapper { width: 90%;
              max-width: 550px;
              margin: 0 auto }

dl { display: flex;
     flex-direction: column }

dl div { flex-direction: row;
         margin: 8px;
         display: flex;}

dt { flex: 1 0 120px }

dd { flex: 1 0 220px;
     margin: 0;}
</style>

<template>
  <div class="wrapper">
    <h2>All Learners</h2>

    <transition name="fade">
      <ul v-if="loaded">
        <LearnerItem v-for="learner in learners"
                     :learner="learner"
                     :key="learner.id" />
      </ul>
    </transition>
  </div>
</template>

<script>
  import LearnerItem from './LearnerItem'

  export default {
    data () {
      return { 'blah': false,
        'loaded': false,
        'learners': [
          { 'name': '',
            'id': 0,
            'slack_name': '',
            'email': '',
            'goal': '' } ] }
    },
    components: { 'LearnerItem': LearnerItem },
    methods: {
      learner_identifier (learner) {
        return learner.name || 'anonymous'
      }
    },
    mounted () {
      fetch('http://localhost:6060/api/learners')
        .then((resp) => resp.json())
        .then((json) => {
          this.learners = json
          this.loaded = true
        })
    }
  }
</script>

<style>
div.wrapper { width: 90%;
              max-width: 550px;
              margin: 0 auto }
</style>

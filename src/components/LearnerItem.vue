<template>
  <li>
    <router-link :to="{ name: 'Learner', params: { id: learner.id } }">
      {{ displayName }}
    </router-link>
    <span class="slack_name"> {{ slackName }} </span>
    <span class="goal"> {{ goal }}</span>
  </li>
</template>

<script>
  export default {
    props: ['learner'],
    computed: {
      displayName () {
        if (this.learner.name) {
          return this.learner.name
        } else {
          return 'Anonymous'
        }
      },
      slackName () {
        if (this.learner.slack_name) {
          return '(' + this.learner.slack_name + ')'
        } else {
          return ''
        }
      },
      goal () {
        if (this.learner.goal) {
          return '—' + this.learner.goal
        } else {
          return ''
        }
      }
    }
  }
</script>

<style>
span.slack_name { margin-left: 8px }
span.goal { margin-left: 8px }
</style>

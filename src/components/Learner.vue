<template>
  <div class="wrapper">
    <h2>Learner Profile: {{ this.learner.name || 'anonymous' }}</h2>

    <transition name="fade">
      <dl v-if="loaded">
        <div>
          <dt>Name</dt>
          <dd>{{ learner.name || 'not provided' }}</dd>
        </div>
        <div>
          <dt>LG Slack name</dt>
          <dd>{{ learner.slack_name || 'not provided' }}</dd>
        </div>
        <div>
          <dt>Goal</dt>
          <dd>{{ learner.goal || 'not provided' }}</dd>
        </div>
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
        'privacy': '',
        'goal': '' },
      'loaded': false
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
dl { display: flex;
     flex-direction: column }

dl div { flex-direction: row;
         margin: 8px;
         display: flex;
         flex-wrap: wrap;
         align-items: center;
         margin: 16px 0 16px 0 }

dl div p { color: darkgrey;
           margin: 8px 0 8px 0; }

dt { flex: 1 0 120px }

dd { flex: 1 0 220px;
     margin: 0 }
</style>

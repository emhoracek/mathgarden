<template>
  <div class="wrapper">
    <h2>Learner Profile: {{ this.title_name }}</h2>

    <transition name="fade">
      <form  v-if="loaded" @submit="submit">
        <dl>
          <div v-if="authed">
            <dt>Email</dt>
            <dd>
              <span>{{ learner.email }}</span>
            </dd>
            <p class="full-width">Your email isn't visible to other learners.</p>
          </div>
          <div>
            <dt><label for="name">Name</label></dt>
            <dd>
              <span v-if="!authed">{{ learner.name || 'not provided' }}</span>
              <input v-if="authed" name="name" v-model="learner.name" />
            </dd>
          </div>
          <div>
            <dt><label for="slack_name">LG Slack name</label></dt>
            <dd>
              <span v-if="!authed">{{ learner.slack_name || 'not provided' }}</span>
              <input v-if="authed" name="slack_name" v-model="learner.slack_name" />
            </dd>
            <p v-if="authed" class="full-width">If you are a <a href="https://lg-slack-automate.herokuapp.com/">Learning Gardens Slack chat</a> user, you can enter your username here.</p>
          </div>
          <div>
            <dt><label for="goal">Goal</label></dt>
            <dd>
              <span v-if="!authed">{{ learner.goal || 'not provided' }}</span>
              <input v-if="authed" name="goal" v-model="learner.goal" />
            </dd>
            <p v-if="authed" class="full-width">Share what you would like to achieve by joining Learning Gardens.</p>
          </div>
        </dl>

        <p class="error errors" v-if="errors.general">
          {{ errors.general }}
        </p>

        <p class="button" v-if="authed">
          <button>Update</button>
        </p>
      </form>
    </transition>
  </div>
</template>

<script>
import Cookie from 'js-cookie'
import base64 from 'base-64'

export default {
  data () {
    return {
      'learner': {
        'name': '',
        'id': 0,
        'email': '',
        'slack_name': '',
        'goal': '' },
      'loaded': false,
      'errors': { },
      'title_name': '',
      'authed_token': Cookie.get('mathgarden_token'),
      'authed_id': Cookie.get('mathgarden_id') }
  },
  computed: {
    authed () {
      return (this.authed_id === String(this.learner.id))
    }
  },
  methods: {
    submit (e) {
      e.preventDefault()
      this.loaded = false
      const token = this.authed_token
      fetch(`http://localhost:6060/api/learners/${this.learner.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' +
            base64.encode(token + ':' + 'tokenpass')
        },
        body: JSON.stringify(this.learner)
      }).then((resp) => {
        return resp.json()
      }).then(this.updateLearner)
        .then(() => { this.loaded = true })
    },
    updateLearner (json) {
      if (json.id) {
        this.learner = json
        this.title_name = json.name || 'anonymous'
      } else {
        this.errors.general = json.error
      }
    }
  },
  mounted () {
    const id = this.$route.params.id
    fetch(`http://localhost:6060/api/learners/${id}`)
      .then((resp) => resp.json())
      .then((json) => {
        this.learner = json
        this.title_name = json.name || 'anonymous'
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
         display: flex;
         flex-wrap: wrap;
         align-items: center;
         margin: 16px 0 16px 0 }

dl div p { color: darkgrey;
           margin: 8px 0 8px 0; }

dt { flex: 1 0 120px }

dd { flex: 1 0 220px;
     margin: 0;}

input { width: calc(100% - 32px) }

p.button { display: flex;
           flex-direction: column }

button { align-self: end }
</style>

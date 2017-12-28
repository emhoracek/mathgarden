<template>
  <div class="wrapper">
    <h2>Edit your profile</h2>

    <transition name="fade">
      <form v-if="loaded"
            @submit="submit">
        <ul>
          <li>
            <label for="email">Email</label>
            <input class="readonly" name="emai" readonly v-model="learner.email" />
            <p class="error full-width" v-if="errors.email">
              {{ errors.email }}
            </p>
          </li>
          <li>
            <label>Name <span class="required">(optional)</span></label>
            <input v-model="learner.name" />
          </li>
          <li>
            <label>LG Slack user <span class="required">(optional)</span></label>
            <input v-model="learner.slack_name" />
            <p class="full-width">If you are a <a href="https://lg-slack-automate.herokuapp.com/">Learning Gardens Slack chat</a> user, you can enter your username here.</p>
          </li>
          <li>
            <label>Goal <span class="required">(optional)</span></label>
            <textarea v-model="learner.goal" />
            <p class="full-width">Share what you would like to achieve by joining Learning Gardens.</p>
          </li>
          <li>
            <label for="privacy" class="full-width">My profile should be:</label>
            <LearnerPrivacyOptions @updatePrivacy="updatePrivacy"
                                   :currentPrivacy="learner.privacy" />
          </li>
        </ul>

        <p class="error errors" v-if="errors.general">
          {{ errors.general }}
        </p>

        <p class="button">
          <button>Update</button>
        </p>
      </form>
    </transition>
  </div>
</template>

<script>
import Cookie from 'js-cookie'
import base64 from 'base-64'
import bus from '../bus'
import LearnerPrivacyOptions from './LearnerPrivacyOptions'

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
      'loaded': false,
      'errors': {
        'email': '',
        'general': ''
      },
      'authed_token': Cookie.get('mathgarden_token'),
      'authed_id': Cookie.get('mathgarden_id') }
  },
  components: { 'LearnerPrivacyOptions': LearnerPrivacyOptions },
  computed: {
    authed () {
      return (this.authed_id === String(this.learner.id))
    }
  },
  methods: {
    submit (e) {
      e.preventDefault()
      this.loaded = false
      let token = this.authed_token
      fetch(`http://localhost:6060/api/learners/me`, {
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
    updatePrivacy (privacy) {
      this.learner.privacy = privacy
    },
    updateLearner (json) {
      if (json.id) {
        this.learner = json
        Cookie.set('mathgarden_token', json.token, { expires: 7 })
        bus.$emit('updateLogin', json.token, json.id)
      } else {
        this.errors.general = json.error
      }
    }
  },
  mounted () {
    let token = this.authed_token
    fetch(`http://localhost:6060/api/learners/me`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' +
          base64.encode(token + ':' + 'tokenpass')
      }})
      .then((resp) => resp.json())
      .then(this.updateLearner)
      .then((r) => { this.loaded = true })
  }
}
</script>

<style>
ul { padding-left: 0 }

li { display: flex;
     flex-wrap: wrap;
     align-items: center;
     margin: 16px 0 16px 0; }

li p { margin: 8px 0 8px 0;
       color: darkgrey }

label { flex: 1 0 120px;
        max-width: 220px;
        display: inline-block }

input { flex: 1 0 220px; }
input.readonly { border: 1px solid white }

textarea { flex: 1 0 220px;
           border: 1px solid black;
           font-size: 16px;
           padding: 8px;
           font-family: 'Helvetica' }

p.button { display: flex;
           flex-direction: column }

button.left { align-self: start }

button { align-self: end }
</style>

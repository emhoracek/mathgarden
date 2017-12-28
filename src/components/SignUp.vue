<template>
  <div class="wrapper">
    <h2>Join the math garden</h2>
    <form @submit="submit">
      <ul>
        <li>
          <label for="email">Email <span class="required">(required)</span></label>
          <input name="emai" v-model="learner.email" />
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
        <button>Create new account</button>
      </p>
    </form>
  </div>
</template>

<script>
  import Cookie from 'js-cookie'
  import bus from '../bus'
  import LearnerPrivacyOptions from './LearnerPrivacyOptions'

  export default {
    data () {
      return {
        learner: {
          email: '',
          slack_name: '',
          name: '',
          goal: '',
          privacy: 'shared'
        },
        errors: {
          email: '',
          general: ''
        }
      }
    },
    components: { 'LearnerPrivacyOptions': LearnerPrivacyOptions },
    computed: {
      emailErrors () {
        const email = this.learner.email
        if (!email) {
          return 'Email is required.'
        }
        if (email && !(email.includes('@'))) {
          return 'Invalid email.'
        }
      }
    },
    methods: {
      validate () {
        return new Promise((resolve, reject) => {
          if (this.emailErrors) {
            this.errors.email = this.emailErrors
            reject(new Error('Invalid email'))
          } else {
            this.errors.email = ''
            resolve('Submit it!')
          }
        })
      },
      updatePrivacy (privacy) {
        this.learner.privacy = privacy
      },
      submit (e) {
        e.preventDefault()
        this.validate()
          .then(this.createLearner)
          .catch((e) => "don't care about this")
      },
      createLearner (result) {
        return fetch('http://localhost:6060/api/learners',
          { method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.learner)
          }).then((resp) => {
            return resp.json()
          }).then((json) => {
            this.errors = {}
            if (json.id) {
              this.setTokenAndIdInCookie(json.token, json.id)
              this.$router.push({ name: 'Learner', params: { 'id': json.id } })
            } else {
              this.errors.general = json.error || 'Please try again.'
            }
          })
      },
      setTokenAndIdInCookie (token, id) {
        Cookie.set('mathgarden_token', token, { expires: 7 })
        Cookie.set('mathgarden_id', id, { expires: 7 })
        bus.$emit('updateLogin', token, id)
        this.logged_in = true
      }
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

textarea { flex: 1 0 220px;
           border: 1px solid black;
           font-size: 16px;
           padding: 8px;
           font-family: 'Helvetica' }

p.button { display: flex;
           flex-direction: column }

button { align-self: end }
</style>

<template>
  <div class="wrapper">
    <h2>Join the math garden</h2>
    <form @submit="submit">
      <ul>
        <li>
          <label for="email">Email: </label>
          <input name="emai" v-model="learner.email" />
          <p class="email-errors" v-if="errors.email">
            {{ errors.email }}
          </p>
        </li>
        <li>
          <label>Name: </label>
          <input v-model="learner.name" />
        </li>
        <li>
          <label>LG Slack name: </label>
          <input v-model="learner.slack_name" />
        </li>
        <li>
          <label>Goal: </label>
          <textarea v-model="learner.goal" />
        </li>
      </ul>
      <p class="button">
        <button>Create new account</button>
      </p>
    </form>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        learner: {
          email: '',
          slack_name: '',
          name: '',
          goal: ''
        },
        errors: {
          email: ''
        }
      }
    },
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
          })
      }
    }
  }
</script>

<style>
div.wrapper { width: 90%;
              max-width: 550px;
              margin: 0 auto }

.email-errors { width: 100%;
                margin: 4px;
                color: red;
                text-align: center }

form { margin: auto }

ul { padding-left: 0 }

ul li { display: flex;
        flex-wrap: wrap;
        align-items: center;
        margin: 8px }

li p { display: block }

label { flex: 1 0 120px;
        max-width: 220px;
        display: inline-block }

input { flex: 1 0 220px;
        border: 1px solid black;
        font-size: 16px;
        padding: 8px }

textarea { flex: 1 0 220px;
           border: 1px solid black;
           font-size: 16px;
           padding: 8px;
           font-family: 'Helvetica' }

p.button { display: flex;
           flex-direction: column }

button { text-align: center;
         align-self: end;
         font-size: 16px;
         padding: 8px;
         margin-right: 8px }

</style>

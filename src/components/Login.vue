<template>
  <div class="wrapper">
    <h2>Login via a magic link</h2>

    <p>Enter your email and we'll send you a link that you can click to login. No password needed.</p>

    <transition name="fade">
      <form v-if="!sent"
            @submit="submit">
        <div>
          <label for="email">Email</label>
          <input name="email" v-model="email" />
          <p class="error full-width" v-if="errors.email">
            {{ errors.email }}
          </p>
        </div>

        <p class="error errors" v-if="errors.general">
          {{ errors.general }}
        </p>

        <p class="button">
          <button>Send magic link</button>
        </p>
      </form>
    </transition>

    <transition name="fade">
      <div v-if="sent">
        <h2>Your magic link has been sent to {{ email }}.</h2>
      </div>
    </transition>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        email: '',
        sent: false,
        errors: {
          email: '',
          general: ''
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
          .then(this.requestMagicLink)
          .catch((e) => "don't care about this")
      },
      requestMagicLink () {
        return fetch('http://localhost:6060/api/magic_links/request', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 'email': this.email })
        }).then((resp) => resp.json())
          .then((r) => {
            if (r.sent) {
              this.sent = true
            } else {
              this.errors.general = 'Unable to send magic link.'
            }
          }).catch(() => { this.errors.general = 'Unable to send magic link.' })
      }
    }
  }
</script>

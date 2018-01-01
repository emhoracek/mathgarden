<template>
  <div class="wrapper">
    <transition name="fade">
      <h2 v-if="!loaded">Logging you in...</h2>
    </transition>
    <transition name="fade">
      <h2 v-if="logged_in">You're logged in!</h2>
    </transition>
    <transition name="fade">
      <div v-if="error">
        <h2>Unable to login...</h2>

        <p>Perhaps this is an old magic link? Try <router-link :to="{ name: 'Login' }">requesting a new one</router-link>.</p>
      </div>
    </transition>
  </div>
</template>

<script>
  import bus from '../bus'
  import Cookie from 'js-cookie'

  export default {
    data () {
      return {
        loaded: false,
        logged_in: false,
        error: '' }
    },
    methods: {
      setTokenAndIdInCookie (token, id) {
        Cookie.set('mathgarden_token', token, { expires: 7 })
        Cookie.set('mathgarden_id', id, { expires: 7 })
        bus.$emit('updateLogin', token, id)
        this.logged_in = true
      }
    },
    mounted () {
      let token = this.$route.params.token
      return fetch(`http://localhost:6060/api/magic_links/verify/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }).then((resp) => resp.json())
        .then((json) => {
          this.errors = ''
          this.loaded = true
          if (json.id) {
            this.setTokenAndIdInCookie(json.token, json.id)
            this.$router.push({ name: 'Learner', params: { 'id': json.id } })
          } else {
            this.error = json.error || 'Please try again.'
          }
        })
    }
  }
</script>

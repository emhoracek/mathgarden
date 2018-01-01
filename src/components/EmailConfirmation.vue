<template>
  <div class="wrapper">
    <transition name="fade">
      <h2 v-if="!loaded">Confirming your email...</h2>
    </transition>
    <transition name="fade">
      <h2 v-if="loaded">Confirmed! Your account is active.</h2>
    </transition>
  </div>
</template>

<script>
  export default {
    data () {
      return { 'loaded': false }
    },
    mounted () {
      let token = this.$route.params.token
      fetch(`http://localhost:6060/api/email_confirmations/${token}`, {
        method: 'POST'
      }).then((resp) => resp.json())
        .then((r) => { this.loaded = true })
    }
  }
</script>

<template>
  <div id="app">
    <header>
      <h1> Math Garden </h1>

      <nav>
        <ul>
          <li><router-link :to="{ name: 'SignUp' }">Sign up</router-link></li>
          <li><router-link :to="{ name: 'Learners' }">Learners</router-link></li>
          <li v-if="loggedIn">
            <router-link :to="{ name: 'LearnerEdit' }">
              My profile
            </router-link>
          </li>
        </ul>
      </nav>
    </header>

    <transition name="flash">
      <div v-if="flashMessage" class="flash">
        <p>
          {{ flashMessage }}
        </p>
      </div>
    </transition>

    <main>
      <router-view/>
    </main>
  </div>
</template>

<script>
   import Cookie from 'js-cookie'
   import bus from './bus.js'

   export default {
     data () {
       return {
         learnerId: Cookie.get('mathgarden_id'),
         loggedIn: Cookie.get('mathgarden_token'),
         flashMessage: ''
       }
     },
     methods: {
       updateLogin (loggedIn, learnerId) {
         this.learnerId = learnerId
         this.loggedIn = loggedIn
       },
       updateFlash (flashMessage) {
         this.flashMessage = flashMessage
         setTimeout(this.clearFlash, 5000)
       },
       clearFlash () {
         this.flashMessage = ''
       },
       blahFlash (m) {
         bus.$emit('updateFlash', m)
       }
     },
     mounted () {
       bus.$on('updateLogin', this.updateLogin)
       bus.$on('updateFlash', this.updateFlash)
     }
   }
</script>

<style>
#app { width: 100vw;
       height: 100vh }

header { padding: 16px;
         padding-left: 24px }

main { display: flex;
       flex-direction: column;
       margin-top: 36px }

div.wrapper { width: 90%;
              max-width: 550px;
              margin: 0 auto }

.fade-enter-active, .fade-leave-active {
    transition: opacity .5s
}
.fade-enter, .fade-leave-to {
    opacity: 0
}

.flash-enter-active, .flash-leave-active {
    transition: opacity .5s
}
.flash-enter, .flash-leave-to {
    opacity: 0
}

.flash { margin: -2px auto;
         position: absolute;
         left: 10%;
         right: 10%;
         border-top: 2px solid black;
         border-radius: 5px;
         background: blue }
.flash p { margin: 16px;
           text-align: center;
           color: white }

header { display: flex;
         flex-direction: row;
         flex-wrap: wrap;
         border: 2px solid black;
         border-width: 0 0 2px 0; }

nav { align-self: center }

nav > ul > li { display: inline-block; margin-left: 16px }

input { border: 1px solid black;
        font-size: 16px;
        padding: 8px }

button { text-align: center;
         font-size: 16px;
         padding: 8px;
         border: 1px solid black;
         border-radius: 5px; }

/* Utility classes */
.error { color: red; }
.full-width { width: 100% }
.required { color: grey }

li { margin: 16px 0 16px 0; }
</style>

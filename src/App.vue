<template>
  <div id="app">
    <header>
      <h1> Math Garden </h1>

      <nav>
        <ul>
          <li><router-link :to="{ name: 'SignUp' }">Sign up</router-link></li>
          <li><router-link :to="{ name: 'Learners' }">Learners</router-link></li>
        </ul>
      </nav>
    </header>

    <main>
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'app'
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

.fade-enter-active, .fade-leave-active {
    transition: opacity .5s
}
.fade-enter, .fade-leave-to {
    opacity: 0
}

header { display: flex;
         flex-direction: row;
         border: 2px solid black;
         border-width: 0 0 2px 0; }

nav { align-self: center }

nav > ul > li { display: inline-block; margin-left: 16px }
</style>

<template>
  <div id="app">
    <header>
      <h1> Math Garden </h1>
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
       flex-direction: column }

</style>

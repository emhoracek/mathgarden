<template>
  <fieldset name="privacy">
    <ul class="inner">
      <li>
        <input id="private"
               value="private"
               type="radio"
               v-model="privacy" />
        <label for="private">Private</label>
      </li>
      <li>
        <input id="shared"
               value="shared"
               type="radio"
               v-model="privacy" />
        <label for="shared">Shared with other learners</label>
      </li>
      <li>
        <input id="public"
               value="public"
               type="radio"
               v-model="privacy" />
        <label for="public">Public</label>
      </li>
    </ul>
  </fieldset>
</template>

<script>
  export default {
    data () {
      return { 'privacy': '' }
    },
    props: ['currentPrivacy'],
    mounted () {
      this.privacy = this.currentPrivacy
    },
    methods: {
      updatePrivacy () {
        this.$emit('updatePrivacy', this.privacy)
      }
    }
  }
</script>

<style>
input[type="radio"] { width: 20px;
                      margin: 0 8px;
                      flex: unset }

fieldset { flex: 1 0 220px;
           border: 1px solid black;
           font-size: 16px;
           padding: 0px }
</style>

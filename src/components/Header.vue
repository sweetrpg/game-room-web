<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="https://sweetrpg.com">
        <img src="/images/sweetrpg-logo.png" alt="SweetRPG" width="112" height="28" />
      </a>
      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item">Home</router-link>
         <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          Applications
        </a>
        <div class="navbar-dropdown">
        <router-link v-if="isAuthenticated" to="/apps" class="navbar-item">Applications</router-link>
        </div>
         </div>

               <div class="navbar-end">
               <div v-if="!isAuthenticated">
        <router-link to="/register" class="navbar-item">Sign-up</router-link>
        <router-link to="/login" class="navbar-item">Login</router-link>
               </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    }
  }
};
</script>

<style>
</style>

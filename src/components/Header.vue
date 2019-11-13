<template>
  <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="https://sweetrpg.com">
        <img src="/static/images/sweetrpg-logo.png" alt="SweetRPG" width="50" height="50" />
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

        <div v-if="isAuthenticated" class="navbar-item has-dropdown is-hoverable">
            <router-link to="/apps" class="navbar-link">Applications</router-link>
            <div class="navbar-dropdown">
              <router-link to="/apps/initiative" class="navbar-item">Initiative!</router-link>
            </div>
        </div>
            <router-link v-if="!isAuthenticated" to="/apps" class="navbar-link">Applications</router-link>
</div>

      <div class="navbar-end">
        <div class="navbar-item" v-if="!isAuthenticated">
          <div class="buttons">
          <a @click="login" class="button is-dark"><strong>Sign up</strong></a>
          <a @click="login" class="button is-dark"><strong>Login</strong></a>
            <!-- <router-link to="/login" class="button is-primary">Sign-up</router-link>
             <router-link to="/login" class="button">Login</router-link> -->
          </div>
        </div>
        <div class="navbar-item has-dropdown is-hoverable" v-if="isAuthenticated">
          <a class="navbar-link is-arrowless">icon</a>
          <div class="navbar-dropdown is-boxed is-right">
            <a class="navbar-item">User's display name</a>
            <a class="navbar-item">Settings</a>
            <hr class="navbar-divider" />
            <a class="navbar-item">Logout</a>
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

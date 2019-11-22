<template>
<div class="header">
  <b-navbar toggleable="md" type="dark" variant="info">
    <b-navbar-brand href="#">
            <a class="navbar-item" href="https://sweetrpg.com">
                <img src="/static/images/sweetrpg-logo-small.png" alt="SweetRPG" width="50" height="50" />
            </a>
            </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#"><router-link to="/" class="navbar-item">Home</router-link></b-nav-item>
        <!-- TODO: slot: current application -->
        <b-nav-item-dropdown text="Applications" right>
          <b-dropdown-item href="#">
                <router-link to="/apps/initiative" class="navbar-item">Initiative!</router-link>
              </b-dropdown-item>
        </b-nav-item-dropdown>
        <!-- <b-nav-item href="#" disabled>Disabled</b-nav-item> -->
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>

        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>
            <img class="avatar" src="https://s.gravatar.com/avatar/692e3236d9415d016ecf01c1c1a15cbc?s=35" alt="User"/>
          </template>
          <b-dropdown-item href="#"><em>User's display name</em></b-dropdown-item>
          <b-dropdown-item href="#">Settings</b-dropdown-item>
           <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
    <!-- <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="https://sweetrpg.com">
                <img src="/static/images/sweetrpg-logo-small.png" alt="SweetRPG" width="50" height="50" />
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
                        <! -- <router-link to="/login" class="button is-primary">Sign-up</router-link>
                        <router-link to="/login" class="button">Login</router-link> -- >
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
        </div>
    </nav> -->
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return false; // this.$store.getters.isAuthenticated;
    }
  },
  methods: {
      login() {

      }
  },
};
</script>

<style>

.header {
    background-color: darkgray;
    font-size: 20px;
}

.avatar {
    border-color: #111111;
    border-width: 5px;
    border-radius: 50%;
}

</style>

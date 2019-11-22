<template>
  <div class="card" style="width: 18rem;">
      <router-link v-bind:to="`initiative/encounter/${encounter.id}`">
    <img src="/static/images/encounter-default.png" class="card-img-top" alt="..." />
    <div class="card-body">
      <h2 class="card-title">{{ name }}</h2>
      <p class="card-text">D&amp;D 5e &mdash; {{ participantCount }} participants</p>
      <p class="card-text">
        <small class="text-muted">Last updated 3 mins ago</small>
      </p>
      <div class="container">
        <div class="left">
          <a href="#" class="btn btn-primary">Open</a>
        </div>
        <div class="right">
          <div class="favorite-button">
            <font-awesome-icon :icon="['fas', 'star']" />
          </div>
          <div class="settings-button">
            <font-awesome-icon :icon="['fas', 'cog']" />
          </div>
        </div>
      </div>
    </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "encounter-item",
  props: {
    encounter: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      id: "",
      name: "Reckoning",
      gameSystem: "dnd5e",
      participantCount: 3,
      isFavorite: false
    };
  }
};
</script>

<style>
</style>

<template>
  <div class="container">
    <div class="row">
      <div class="card" style="width: 18rem;" v-for="app in apps" v-bind:key="app.slug">
        <router-link v-bind:to="app.route">
          <img src="/static/images/app-initiative-small.png" class="card-img-top" alt="..." />
          <div class="card-body">
            <h1 class="card-title">{{ app.name }}</h1>
            <p class="card-text">{{ app.description }}</p>
            <a href="#" class="btn btn-primary">Use</a>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "app-list",
  data() {
    return {
      apps: [
        {
          slug: "initiative",
          name: "Initiative!",
          description: "An encounter tracker",
          route: "/apps/initiative"
        }
      ]
    };
  }
};
</script>

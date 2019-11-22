<template>
  <b-button-toolbar>
    <b-button id="next-participant" variant="outline" v-b-tooltip.hover title="Advance to the next participant">
      <img src="/static/images/button-next-participant.png" />
    </b-button>
    <b-button id="collect-initiative" variant="outline-success" v-b-tooltip.hover title="Collect initiative values">
      <img src="/static/images/button-collect-initiative.png" />
    </b-button>
  </b-button-toolbar>
</template>

<script>
export default {
  name: "control-bar",
  data() {
    return {};
  }
};
</script>

<style>
button {
  border: 0;
}
</style>

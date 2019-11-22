<template>
  <div class="container">
    <div class="row">
      <encounter-item v-for="encounter in encounters" :encounter="encounter" :key="encounter.id" />
    </div>
  </div>
</template>

<script>
import EncounterItem from "./EncounterItem.vue";

export default {
  name: "encounter-list",
  components: {
    "encounter-item": EncounterItem
  },
  data() {
    return {
      encounters: [
        {
          id: "1",
          name: "TODO",
          gameSystem: "dnd5e",
          participantCount: 3,
          isFavorite: false
        }
      ]
    };
  }
};
</script>

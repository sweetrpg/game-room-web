<template>
  <div>
    <encounter-list />
  </div>
</template>

<script>
import EncounterList from "./EncounterList";

export default {
  name: "initiative",
  components: {
    "encounter-list": EncounterList
  },
  data() {
    return {
    }
  }
}
</script>

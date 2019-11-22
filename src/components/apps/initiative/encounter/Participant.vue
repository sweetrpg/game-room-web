<template>
  <tr class="participant-row">
    <td class="container participant-initiative">
      <!-- TODO: on-click: create input box -->
      {{ participant.initiative }}
    </td>
    <td class="container participant-type">
      <!-- TODO: on-click: create popup -->
      {{ participant.type }}
    </td>
    <td class="container participant-name">
      <!-- TODO: on-click: create input box -->
      <h3>{{ participant.name }}</h3>
      <br />
      <div class="container participant-tags">
        <!-- TODO: on-click: create input box for tags -->
        {{ participant.tags }}
      </div>
    </td>
    <td class="container participant-health">
      <!-- TODO: on-click: dialog for health input -->
      {{ participant.health }}
    </td>
    <td class="container participant-notes">
      <!-- TODO: on-click: dialog -->
      {{ participant.notes }}
    </td>
    <td class="drag-handle"></td>
  </tr>
</template>

<script>
export default {
  name: "participant",
  props: ["participant"],
  data() {
    return {
      participant: {}
    };
  }
};
</script>

<style>
.participant-row {
  background-color: orange;
  border-radius: 10px;
}
.participant-initiative {
  width: 50px;
}
.participant-type {
  width: 60px;
}
.participant-health {
  background-color: green;
}
.participant-notes {
}
.participant-tags {
}
.participant-name {
}
</style>

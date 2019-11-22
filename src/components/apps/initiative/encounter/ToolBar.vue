<template>
  <b-button-toolbar justify key-nav>
    <b-button-group>
      <b-button variant="outline" v-b-tooltip.hover title="Add a participant">
        <b-img src="/static/images/button-add-participant.png" />
      </b-button>
    </b-button-group>
    <b-button-group>
      <b-dropdown variant="outline-danger" v-b-tooltip.hover title="Reset/clear the encounter">
        <template v-slot:button-content>
          <b-img src="/static/images/button-reset.png" />
        </template>
        <b-dropdown-item v-b-tooltip.hover title="Reset all participant initiative to 0">
          <b-img src="/static/images/button-reset.png" />Reset Participants
        </b-dropdown-item>
        <b-dropdown-divider />
        <b-dropdown-item v-b-tooltip.hover title="Remove all non-PC participants">
          <b-img src="/static/images/button-clear.png" />Everything but the PCs
        </b-dropdown-item>
        <b-dropdown-item v-b-tooltip.hover title="Remove all participants">
          <b-img src="/static/images/button-clear.png" />Everything!
        </b-dropdown-item>
      </b-dropdown>
    </b-button-group>
    <b-button-group>
      <b-dropdown variant="outline" v-b-tooltip.hover title="Encounter actions">
        <template v-slot:button-content>
          <b-img src="/static/images/button-actions.png" />
        </template>
        <b-dropdown-item v-b-tooltip.hover title="Sort the list of participants according to their current initiative value">
          <b-img src="/static/images/button-sort-participants.png" />Sort Participants
        </b-dropdown-item>
        <b-dropdown-item v-b-tooltip.hover title="Mark this encounter as a favorite">
          <b-img src="/static/images/button-favorite-off.png" />Favorite
        </b-dropdown-item>
        <b-dropdown-divider />
        <b-dropdown-item v-b-tooltip.hover title="Edit the encounter's settings">
          <b-img src="/static/images/button-actions.png" />Encounter Settings
        </b-dropdown-item>
      </b-dropdown>
    </b-button-group>
  </b-button-toolbar>
</template>

<script>
export default {
  name: "toolbar",
  data() {
    return {};
  }
};
</script>

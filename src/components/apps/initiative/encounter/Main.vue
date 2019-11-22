<template>
  <!--
    toolbars
    list of participants
    advancement controls
  -->
  <b-container>
    <b-row>
      <b-col sm="2">
        <toolbar />
      </b-col>
      <b-col>
        <b-row align-h="end">
          <control-bar />
        </b-row>
        <b-row>
          <participant-list />
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ControlBar from "./ControlBar";
import ToolBar from "./ToolBar";
import ParticipantList from "./ParticipantList";

export default {
  name: "encounter",
  props: ["id"],
  components: {
    "control-bar": ControlBar,
    toolbar: ToolBar,
    "participant-list": ParticipantList
  },
  data() {
    return {};
  }
};
</script>

<style>
#encounter-controls {
}
</style>

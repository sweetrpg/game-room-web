<template>
  <b-container>
    <b-row>
      <b-table-simple hover responsive>
        <b-tbody>
          <draggable>
            <b-tr v-for="participant in participants" class="participant-row" :key="participant.id">
              <b-td class="container participant-initiative">
                <!-- TODO: on-click: create input box -->
                {{ participant.initiative }}
              </b-td>
              <b-td class="container participant-type">
                <!-- TODO: on-click: create popup -->
                {{ participant.type }}
              </b-td>
              <b-td class="container participant-name">
                <!-- TODO: on-click: create input box -->
                <h3>{{ participant.name }}</h3>
                <br />
                <div class="container participant-tags">
                  <!-- TODO: on-click: create input box for tags -->
                  {{ participant.tags }}
                </div>
              </b-td>
              <b-td class="container participant-health">
                <!-- TODO: on-click: dialog for health input -->
                {{ participant.health }}
              </b-td>
              <b-td class="container participant-notes">
                <!-- TODO: on-click: dialog -->
                {{ participant.notes }}
              </b-td>
              <b-td class="drag-handle">
                <font-awesome-icon icon="bars"></font-awesome-icon>
              </b-td>
            </b-tr>
          </draggable>
        </b-tbody>
      </b-table-simple>
      <!-- <b-table hover :items="participants" :fields="fields" :sort-by="order"></b-table> -->
      <!-- TODO: use b-table-simple? -->
    </b-row>
  </b-container>
</template>

<script>
// import Participant from "./Participant";
import Draggable from "vuedraggable";

export default {
  name: "participant-list",
  components: {
    // participant: Participant,
    draggable: Draggable
  },
  data() {
    return {
      fields: [
        {
          key: "initiative",
          sortable: true
        },
        {
          key: "type",
          sortable: false
        },
        {
          key: "name",
          sortable: false
        },
        {
          key: "health",
          sortable: false
        },
        {
          key: "notes",
          sortable: false
        }
      ],
      participants: [
        {
          id: "1",
          name: "Bartholomew",
          type: "pc",
          order: 0,
          initiative: "15",
          health: {},
          notes: ""
        },
        {
          id: "2",
          name: "Calencela",
          type: "pc",
          order: 1,
          initiative: "15",
          health: {},
          notes: ""
        },
        {
          id: "3",
          name: "Grom",
          type: "pc",
          order: 7,
          initiative: "15",
          health: {},
          notes: ""
        },
        {
          id: "4",
          name: "Rorrim",
          type: "pc",
          order: 4,
          initiative: "15",
          health: {},
          notes: ""
        },
        {
          id: "5",
          name: "Strelok",
          type: "pc",
          order: 17,
          initiative: "15",
          health: {},
          notes: ""
        }
      ]
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

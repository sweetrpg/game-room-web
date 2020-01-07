
// $("#create-group-button").click(function () {
//   $("#create-group-modal").modal({ show: true });
// });

Vue.config.devtools = true;
// Vue.use(Vuex);

const storeState = {
  encounters: [],
  groups: [],
  gameSystems: [],
};
const storeActions = {
  fetchGameSystems(context) {
    axios.get('/api/v1/gamesystems')
      .then((response) => {
        // handle success
        console.log(response);
        context.commit('setGameSystems', { gameSystems: response.data.game_systems })
      })
      .catch((error) => {
        // handle error
        console.log(error);
      })
      .finally(() => {
        // always executed
      });
  },
  fetchEncounters(context) {
    axios.get('/api/v1/encounters')
      .then((response) => {
        // handle success
        console.log(response);
        context.commit('setEncounters', { encounters: response.data.encounters })
      })
      .catch((error) => {
        // handle error
        console.log(error);
      })
      .finally(() => {
        // always executed
      });
  },
  fetchGroups(context) {
    axios.get('/api/v1/groups')
      .then((response) => {
        // handle success
        console.log(response);
        context.commit('setGroups', { groups: response.data.groups })
      })
      .catch((error) => {
        // handle error
        console.log(error);
      })
      .finally(() => {
        // always executed
      });
  }
};
const storeMutations = {
  setGameSystems: function (state, payload) {
    console.log(payload);
    state.gameSystems = payload.gameSystems;
  },
  setEncounters: function (state, payload) {
    console.log(payload);
    state.encounters = payload.encounters;
  },
  setGroups: function (state, payload) {
    console.log(payload);
    state.groups = payload.groups;
  }
};
const storeGetters = {

};

const store = new Vuex.Store({
  state: storeState,
  actions: storeActions,
  mutations: storeMutations,
  getters: storeGetters,
});

const vm = new Vue({
  el: '#app',
  store: store,
  components: {
    'encounter-list': EncounterList,
    'create-encounter-dialog': CreateEncounterDialog,
    'create-group-dialog': CreateGroupDialog,
  },
  data: {
  },
});

window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = vm.constructor

$('#createEncounterDialog').on('shown.bs.modal', function () {
  $('#createEncounterName').focus();
  $('#createEncounterProgress').hide();
  $('#createEncounterFeedback')
    .removeClass('alert-danger').removeClass('alert-success')
    .html(``).hide();
})
$('#createGroupDialog').on('shown.bs.modal', function () {
  $('#createGroupName').focus();
  $('#createGroupProgress').hide();
  $('#createGroupFeedback')
    .removeClass('alert-danger').removeClass('alert-success')
    .html(``).hide();
})

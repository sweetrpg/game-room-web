
// $("#create-group-button").click(function () {
//   $("#create-group-modal").modal({ show: true });
// });

Vue.config.devtools = true;
// Vue.use(Vuex);

const storeState = {
  encounters: [],
  gameSystems: [],
};
const storeActions = {
  fetchGameSystems(context) {
    axios.get('/api/v1/gamesystems')
      .then(function (response) {
        // handle success
        console.log(response);
        context.commit('setGameSystems', { gameSystems: response.data.game_systems })
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .finally(function () {
        // always executed
      });
  },
  fetchEncounters(context) {
    axios.get('/api/v1/encounters')
      .then(function (response) {
        // handle success
        console.log(response);
        context.commit('setEncounters', { encounters: response.data.encounters })
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .finally(function () {
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
  $('#encounterName').focus();
})

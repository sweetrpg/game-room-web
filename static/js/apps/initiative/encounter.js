
// TODO: this should be looked-up per locale
const participantTypeMap = {
'pc': 'Player Character',
'adversary': 'Adversary',
'object': 'Object',
}

Vue.config.devtools = true;

const storeState = {
    encounter: {},
    currentParticipant: null,
    currentParticipantIndex: -1,
    messages: [], // { type: '<type>', message: '<text>' }
};
const storeActions = {
    addMessage(context, payload) {
        context.commit('addMessage', { type: payload.type || 'danger', message: payload.message })
    },
    removeMessage(context, payload) {
        context.commit('removeMessage', { messageId: payload.messageId })
    },
    clearMessages(context) {
        context.commit('clearMessages')
    },
    fetchEncounter(context) {
        const encounterId = $('data#encounterId').val();
        console.log("encounterId", encounterId);
        axios.get('/api/v1/encounters/' + encounterId)
            .then(function (response) {
                // handle success
                console.log(response);
                context.commit('setEncounter', { encounter: response.data })
            })
            .catch(function (error) {
                // handle error
                console.log(error);
                context.commit('addMessage', { type: 'danger', message: error })
            })
            .finally(function () {
                // always executed
            });
    },
    setCurrentParticipant(context, payload) {
        console.log('setCurrentParticipant', context, payload)
        context.commit('setCurrentParticipant', {
            participant: payload.participant,
            index: payload.index,
         })
    }
};
const storeMutations = {
    setCurrentParticipant(state, payload) {
        // console.log(payload);
        var index = payload.index;
        var participant = payload.participant;

        if (index === undefined) {
            console.log("trying to determine index of participant, since it wasn't provided", state.encounter)
            index = state.encounter.encounter.participants.indexOf(payload.participant)
        }
        else if (participant === undefined) {
            console.log("trying to determine participant from index, since it wasn't provided", state.encounter)
            participant = state.encounter.encounter.participants[index];
        }

        state.currentParticipant = participant;
        state.currentParticipantIndex = index;
    },
    addMessage(state, payload) {
        console.log(payload);
        const messageId = state.messages.length;
        state.messages.push({
            id: messageId,
            type: payload.type,
            message: payload.message,
        });
    },
    removeMessage(state, payload) {

    },
    clearMessages(state, payload) {
        state.messages = []
    },
    setEncounter(state, payload) {
        console.log(payload);
        state.encounter = payload.encounter;
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
        'draggable': vuedraggable,
        'messages': Messages,
        'encounter-info': EncounterInfo,
        'encounter-toolbar': EncounterToolbar,
        'encounter-action-bar': EncounterActionBar,
        'encounter-participant-list': EncounterParticipantList,
        'add-participant-dialog': AddParticipantDialog,
        'delete-participant-dialog': DeleteParticipantDialog,
        'edit-participant-dialog': EditParticipantDialog,
        'edit-participant-order-dialog': EditParticipantOrderDialog,
        'collect-initiative-dialog': CollectInitiativeDialog,
    },
    data: {
    },
    methods: {
        updateList() {
            console.log("updateList")
        },
        chooseParticipant() {
            console.log("chooseParticipant")
        }
    },
    beforeMount() {
        console.log("encounter.js beforeMount")
        this.$store.dispatch('fetchEncounter')
    },
});

window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = vm.constructor

$('#addParticipantDialog').on('shown.bs.modal', function () {
    $('#addParticipantName').focus();
})
$('#editParticipantDialog').on('shown.bs.modal', function () {
    $('#editParticipantName').focus();
})
$('#editParticipantOrderDialog').on('shown.bs.modal', function () {
    $('#editParticipantOrderValue').focus();
})
$('#collectInitiativeDialog').on('shown.bs.modal', function () {
    $('#collectInitiativeValue').focus();
})

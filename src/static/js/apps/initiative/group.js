
// TODO: this should be looked-up per locale
const participantTypeMap = {
    'pc': 'Player Character',
    'adversary': 'Adversary',
    'object': 'Object',
}

Vue.config.devtools = true;

const storeState = {
    group: {},
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
    fetchGroups(context) {
        axios.get('/api/v1/groups')
            .then((response) => {
                console.log(response);
                context.commit('setGroups', { groups: response.data })
            })
            .catch((error) => {
                // handle error
                console.log(error);
                context.commit('addMessage', { type: 'danger', message: error })
            })
            .finally(() => {
                // always executed
            });
    },
    fetchGroup(context) {
        const groupId = $('data#groupId').val();
        console.log("groupId", groupId);
        axios.get('/api/v1/groups/' + groupId)
            .then((response) => {
                // handle success
                console.log(response);
                context.commit('setGroup', { group: response.data })
            })
            .catch((error) => {
                // handle error
                console.log(error);
                context.commit('addMessage', { type: 'danger', message: error })
            })
            .finally(() => {
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
            console.log("trying to determine index of participant, since it wasn't provided", state.group)
            index = state.group.participants.indexOf(payload.participant)
        }
        else if (participant === undefined) {
            console.log("trying to determine participant from index, since it wasn't provided", state.group)
            participant = state.group.participants[index];
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
    setGroup(state, payload) {
        console.log(payload);
        state.group = payload.group;
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
        'group-info': GroupInfo,
        'group-toolbar': GroupToolbar,
        'group-participant-list': GroupParticipantList,
        'add-participant-dialog': AddParticipantDialog,
        'delete-participant-dialog': DeleteParticipantDialog,
        'edit-participant-dialog': EditParticipantDialog,
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
        console.log("group.js beforeMount")
        this.$store.dispatch('fetchGroup')
    },
});

window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = vm.constructor

$('#addParticipantDialog').on('shown.bs.modal', function () {
    $('#addParticipantName').focus();
    $('#addParticipantProgress').hide();
    $('#addParticipantFeedback')
        .removeClass('alert-danger').removeClass('alert-success')
        .html(``).hide();
})
$('#editParticipantDialog').on('shown.bs.modal', function () {
    $('#editParticipantName').focus();
    $('#editParticipantProgress').hide();
    $('#editParticipantFeedback')
        .removeClass('alert-danger').removeClass('alert-success')
        .html(``).hide();
})

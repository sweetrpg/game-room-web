
const Messages = {
    name: 'messages',
    components: {
    },
    computed: {
        messages() {
            return this.$store.state.messages;
        }
    },
    data() {
        return {
        };
    },
    template: `
<div class="container">
    <div v-for="m in messages" v-bind:class="'alert alert-' + m.type" role="alert">
        {{ m.message }}
    </div>
</div>
`
}

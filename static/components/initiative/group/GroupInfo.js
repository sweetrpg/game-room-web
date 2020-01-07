
const GroupInfo = {
    name: 'group-info',
    components: {
    },
    computed: {
        encounter() {
            return this.$store.state.group;
        }
    },
    data() {
        return {
        };
    },
    watch: {
        'this.$store.state.group'() {
console.log("$store group updated");
        },
    },
    template: `
<div class="container">
<div class="row">
<h1 class="col-8">
{{ group.name }}
</h1>

<div class="col text-right">
{{ group.participants.length }} participant{{ group.participants.length == 1 ? '' : 's' }}
</div>
</div>
</div>
`
}

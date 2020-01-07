
const GroupSelectorItem = {
    name: 'group-selector-item',
    components: {
    },
    props: {
group: {
            type: Object,
            required: true
},
expanded: {
type: Boolean
}
    },
    data() {
        return {
        }
    },
    computed: {
    },
    methods: {
    },
    beforeMount() {
    },
    template: `
 <div class="container">
 {{ group.name }}

 <ul class="list-group list-group-flush">
  <li v-for="p in group.participants" v-bind:key="p.id"
      class="list-group-item">Dapibus ac facilisis in</li>
</ul>
  </div>
`
}

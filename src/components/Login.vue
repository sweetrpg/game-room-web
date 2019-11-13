<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Login or Register</h2>
                    <p class="subtitle error-msg">{{ errorMsg }}</p>
                </div>
            </div>
        </section>
        <section class="section">
            <div class="container">

            </div>
        </section>
    </div>
</template>

<script>
import { EventBus } from '@/utils'
export default {
    data() {
        return {
            email: '',
            password: '',
            errorMsg: '',
        }
    },
    methods: {
        authenticate() {
            this.$store
                .dispatch('login', {
                    email: this.email,
                    password: this.password,
                })
                .then(() => this.$router.push('/'))
        },
        register() {
            this.$store
                .dispatch('register', {
                    email: this.email,
                    password: this.password,
                })
                .then(() => this.$router.push('/'))
        },
    },
    mounted() {
        EventBus.$on('failedRegistration', (msg) => {
            this.errorMsg = msg
        })
        EventBus.$on('failedAuthentication', (msg) => {
            this.errorMsg = msg
        })
    },
    beforeDestroy() {
        EventBus.$off('failedRegistration')
        EventBus.$off('failedAuthentication')
    },
}
</script>

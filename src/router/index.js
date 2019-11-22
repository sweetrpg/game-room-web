import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import InitiativeApp from '@/components/apps/initiative/Main'
import Encounter from '@/components/apps/initiative/encounter/Main'
// import Survey from '@/components/Survey'
// import NewSurvey from '@/components/NewSurvey'
// import Login from '@/components/Login'
import store from '@/store'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home,
        },
        {
            path: '/apps/initiative',
            name: 'Initiative!',
            component: InitiativeApp,
        },
        {
            path: '/apps/initiative/encounter/:id',
            name: 'Encounter',
            component: Encounter,
        },
        // {
        //     path: '/surveys/:id',
        //     name: 'Survey',
        //     component: Survey,
        // },
        // {
        //     path: '/surveys',
        //     name: 'NewSurvey',
        //     component: NewSurvey,
        //     beforeEnter(to, from, next) {
        //         if (!store.getters.isAuthenticated) {
        //             next('/login')
        //         } else {
        //             next()
        //         }
        //     },
        // },
        // {
        //     path: '/login',
        //     name: 'Login',
        //     component: Login,
        // },
    ],
})

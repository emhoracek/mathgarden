import Vue from 'vue'
import Router from 'vue-router'
import SignUp from '@/components/SignUp'
import Learners from '@/components/Learners'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: SignUp
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    }, /*
    {
      path: '/login',
      name: 'Login',
      component: Login
    }, */
    {
      path: '/learners',
      name: 'Learners',
      component: Learners
    } /* ,
    {
      path: '/learners/:id',
      name: 'LearnerProfile',
      component: LearnerProfile
    },
    {
      path: '/learners/:id/checkins',
      name: 'LearnerCheckins',
      component: LearnerCheckins
    },
    {
      path: '/checkins',
      name: 'Checkins',
      component: Checkins
    } */
  ]
})

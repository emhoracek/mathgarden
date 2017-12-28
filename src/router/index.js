import Vue from 'vue'
import Router from 'vue-router'
import SignUp from '@/components/SignUp'
import Learners from '@/components/Learners'
import Learner from '@/components/Learner'
import LearnerEdit from '@/components/LearnerEdit'

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
    },
    {
      path: '/learners/me',
      name: 'LearnerEdit',
      component: LearnerEdit
    },
    {
      path: '/learners/:id',
      name: 'Learner',
      component: Learner
    } /*,
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

import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import Award from "../components/award/Award.vue";
import Login from "../components/registration/Login.vue";
import Logout from "/src/components/registration/Logout.vue";
import Event from "../components/event/Event.vue";
import EventAttendedStudent from '/src/components/event/EventAttendedStudent.vue'
import Project from "/src/components/project/Project.vue";
import Skill from "/src/components/profile/Skill.vue";
import Skillgroup from "/src/components/profile/Skillgroup.vue";
import Curriculum from "/src/components/profile/Curriculum.vue"
import SkillChartView from "/src/components/profile/skillchart/SkillChartView.vue"
import EventSummary from "/src/components/event/event-summary/EventSummary.vue"
Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/award",
      name: "award",
      component: Award,
    },
    {
      path: "/login-vue",
      name: "login-vue",
      component: Login,
    },
    {
      path: "/logout",
      name: "logout",
      component: Logout,
    },
    {
      path: "/event",
      name: "event",
      component: Event,
    },
    {
      path: "/event/event-attended-student",
      name: "event-attended-student",
      component: EventAttendedStudent,
    },
    {
      path: "/project",
      name: "project",
      component: Project,
    },
    {
      path: "/skill",
      name: "skill",
      component: Skill,
    },
    {
      path: "/skillgroup",
      name: "skillgroup",
      component: Skillgroup,
    },
    {
      path: "/curriculum",
      name: "curriculum",
      component: Curriculum,
    },
    {
      path: "/skillchart",
      name: "skillchart",
      component: SkillChartView,
    },
    {
      path: "/event-summary",
      name: "event-summary",
      component: EventSummary,
    },
  ],
});

export default router;

<template>
    <div>
        <!-- <p>{{ user.is_authenticated }}</p> -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark flex-lg-column flex-lg-row"
            style="position: sticky; top: 0;">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Student Profile Management</a>
            </div>
        </nav>
        <div class="container-fluid h-100 custom-container-fluid">
            <div class="row h-100">

                <div class="col-md-2 d-none d-md-block bg-light sidebar" style="width: 280px; flex-direction: column;">
                    <div class="sidebar-sticky">
                        <ul class="list-unstyled ps-0">
                            <li class="mb-1">
                                <button class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#home-collapse" aria-expanded="true">
                                    Home
                                </button>
                                <div class="collapse show" id="home-collapse">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li><router-link to="/home" class="link-dark rounded">home</router-link></li>
                                    </ul>
                                </div>
                            </li>
                            <li class="mb-1">
                                <button class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="false">
                                    Project
                                </button>
                                <div class="collapse" id="orders-collapse">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li v-if="user.is_authenticated"><router-link to="/project"
                                                class="link-dark rounded">Project</router-link></li>

                                    </ul>
                                </div>
                            </li>
                            <li class="mb-1">
                                <button class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false">
                                    Event
                                </button>
                                <div class="collapse" id="dashboard-collapse">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li v-if="user.is_authenticated"><router-link to="/event"
                                                class="link-dark rounded">Event</router-link></li>
                                        <li v-if="user.is_staff"><router-link to="/event-summary"
                                                class="link-dark rounded">Event Summary</router-link></li>
                                        <li v-if="user.is_student"><router-link to="/event/event-attended-student"
                                                class="link-dark rounded">Event
                                                Attended
                                                Student</router-link></li>

                                    </ul>
                                </div>
                            </li>
                            <li class="mb-1">
                                <button class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#orders-collapse-2" aria-expanded="false">
                                    Award
                                </button>
                                <div class="collapse" id="orders-collapse-2">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li v-if="user.is_authenticated">
                                            <router-link to="/award" class="link-dark rounded">Award</router-link>
                                        </li>
                                        <!-- <li><a href="#" class="link-dark rounded">New</a></li> -->
                                    </ul>
                                </div>
                            </li>
                            <li class="mb-1">
                                <button class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#Profile-collapse" aria-expanded="false">
                                    Profile
                                </button>
                                <div class="collapse" id="Profile-collapse">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li v-if="user.is_student"><router-link to="/skillchart"
                                                class="link-dark rounded">Skill
                                                Chart</router-link></li>
                                        <li v-if="user.is_staff"><router-link to="/skill"
                                                class="link-dark rounded">Skill</router-link></li>
                                        <li v-if="user.is_staff"><router-link to="/skillgroup"
                                                class="link-dark rounded">Skillgroup</router-link>
                                        </li>
                                        <li v-if="user.is_staff"><router-link to="/curriculum"
                                                class="link-dark rounded">Curriculum</router-link>
                                        </li>
                                        <!-- <li><a href="#" class="link-dark rounded">Overview</a></li> -->
                                    </ul>
                                </div>
                            </li>


                            <li class="border-top my-3"></li>
                            <li class="mb-1">
                                <button v-if="!user.is_authenticated" class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#account-collapse" aria-expanded="false">
                                    Account
                                </button>
                                <button v-if="user.is_authenticated" class="btn btn-toggle align-items-center rounded collapsed"
                                    data-bs-toggle="collapse" data-bs-target="#account-collapse" aria-expanded="false">
                                    {{ user.username }}
                                </button>
                                <div class="collapse" id="account-collapse">
                                    <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                                        <li v-if="!user.is_authenticated"><router-link to="/login-vue"
                                                class="link-dark rounded">Login</router-link>
                                        </li>
                                        <li v-if="user.is_authenticated"><router-link to="/logout"
                                                class="link-dark rounded">Logout</router-link>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                        </ul>
                    </div>

                </div>

                <div class="col-lg-10">
                    <router-view />
                </div>
            </div>
        </div>



    </div>
</template>

<script>
import axios from "axios";
import * as bootstrap from "bootstrap"; //where is bootstrap-icons??

export default {
    components: {

    },

    data() {
        return {
            user: null,
        }
    },

    created: async function () {
        await axios.get(this.$API_URL + "user").then((response) => {
            this.user = response.data;
            // console.log(this.user)
        });
    },
}
</script>
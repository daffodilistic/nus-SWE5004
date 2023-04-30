<template>
  <q-page class="bg-grey-10">
    <div class="row fixed-center">
      <div class="col column">
        <h4 class="q-my-sm self-center text-white">MarioToilet Login</h4>
        <h6 class="q-my-sm self-center text-white">Please Login</h6>
        <q-input
          dark
          filled
          v-model="username"
          label="Username *"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        />
        <q-input
          dark
          filled
          v-model="password"
          label="Password *"
          :type="isPwd ? 'password' : 'text'"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        >
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>
        <q-btn @click="onLogin" color="primary" label="login"></q-btn>
        <q-space class="q-my-sm" />
        <q-btn flat to="/" color="secondary" label="Back" />
      </div>
    </div>
  </q-page>
</template>

<style lang="sass" scoped>
.user-profile
  width: 100%
  height: 100%
  max-height: 250px
  max-width: 250px
</style>

<script>
import { defineComponent, ref } from "vue";
import { useQuasar } from "quasar";
import { api } from "boot/axios";
import { useRouter } from 'vue-router';

export default defineComponent({
  name: "LoginPage",
  setup() {
    const $router = useRouter();
    const $q = useQuasar();
    const username = ref(null);
    const password = ref(null);
    let isPwd = ref(true);
    // declaring a variable for notification so that it can be updated
    let notif = null;

    const login = () => {
      api
        .post(
          "/login",
          {
            username: username.value,
            password: password.value,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          if (response !== null && response.lastRowId !== null) {
            notif({
              timeout: 1,
              spinner: false,
              message: "Login successful",
              caption: "100%",
            });
            // Store response in session storage
            sessionStorage.setItem("user", JSON.stringify(response));
            // Navigate to Profiles page
            $router.push("/profiles");
          } else {
            notif({
              timeout: 1,
              color: "negative",
              spinner: false,
              message: "Login failed",
              caption: "100%",
            });
          }
        })
        .catch((e) => {
          // print error to console
          console.error(e);
          if (e.response.status === 401) {
            notif({
              timeout: 1,
              color: "negative",
              spinner: false,
              message: "Login failed",
              caption: "100%",
            });
          } else {
            $q.notify({
              color: "negative",
              position: "top",
              message: "Loading failed",
              icon: "report_problem",
            });
          }
        });
    };

    return {
      username,
      password,
      isPwd,
      onLogin() {
        notif = $q.notify({
          group: false, // required to be updatable
          timeout: 0, // we want to be in control when it gets dismissed
          spinner: true,
          message: "Logging in...",
          caption: "0%",
        });
        login();
      },
    };
  },
});
</script>

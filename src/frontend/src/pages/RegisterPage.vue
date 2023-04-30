<template>
  <q-page class="bg-grey-10">
    <div class="row fixed-center">
      <div class="col column">
        <h4 class="q-my-sm self-center text-white">
          MarioToilet Account Registration
        </h4>
        <div class="q-pa-md" style="max-width: 400px">
          <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
            <q-input
              dark
              filled
              v-model="username"
              label="Username *"
              hint="This will be your display name"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />
            <q-input
              dark
              filled
              v-model="password"
              label="Password *"
              :type="isPwd ? 'password' : 'text'"
              hint="A strong password is recommended"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            >
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
            <q-toggle
              dark
              class="text-white"
              v-model="accept"
              label="I accept the license and terms"
            />
            <div>
              <q-btn label="Submit" type="submit" color="primary" />
              <q-btn
                label="Reset"
                type="reset"
                color="primary"
                flat
                class="q-ml-sm"
              />
              <q-space class="q-my-sm" />
              <q-btn flat to="/" color="secondary" label="Back" />
            </div>
          </q-form>
        </div>
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

export default defineComponent({
  name: "RegisterPage",
  setup() {
    const $q = useQuasar();
    const username = ref(null);
    const password = ref(null);
    const accept = ref(false);
    let isPwd = ref(true);
    // declaring a variable for notification so that it can be updated
    let notif = null;

    const register = () => {
      api
        .post(
          "/register",
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
              message: "Registration successful",
              caption: "100%",
            });
            // Store response in session storage
            sessionStorage.setItem("user", JSON.stringify(response));
            // Navigate to Profiles page
            this.$router.push("/profiles");
          } else {
            $q.notify({
              color: "negative",
              position: "top",
              message: "Registration failed",
              icon: "report_problem",
            });
          }
        })
        .catch((e) => {
          // print error to console
          console.error(e);
          $q.notify({
            color: "negative",
            position: "top",
            message: "Loading failed",
            icon: "report_problem",
          });
        });
    };

    return {
      username,
      password,
      isPwd,
      accept,
      onSubmit() {
        if (accept.value !== true) {
          $q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: "You need to accept the license and terms first",
          });
        } else {
          notif = $q.notify({
            group: false, // required to be updatable
            timeout: 0, // we want to be in control when it gets dismissed
            spinner: true,
            message: "Registering...",
            caption: "0%",
          });
          register();
        }
      },
      onReset() {
        username.value = null;
        password.value = null;
        accept.value = false;
      },
    };
  },
});
</script>

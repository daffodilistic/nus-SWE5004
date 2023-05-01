<template>
  <q-page class="bg-grey-10">
    <div class="row fixed-center">
      <div class="col column">
        <h4 class="q-my-sm self-center text-white">Welcome to MarioToilet</h4>
        <h6 class="q-my-sm self-center text-white">Please select an option</h6>
        <q-btn to="/login" color="primary" label="login"></q-btn>
        <q-space class="q-my-sm" />
        <q-btn @click="register" color="secondary" label="register"></q-btn>
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
import { defineComponent, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "IndexPage",
    setup() {
        const $router = useRouter();
        onMounted(async () => {
            // If logged in, redirect to profile select page
            if (sessionStorage.getItem("account")) {
                $router.replace("/profiles");
            }
        });
    },
    methods: {
        register() {
            this.$router.push("/register");
        },
    }
});
</script>

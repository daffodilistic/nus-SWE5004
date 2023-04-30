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
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "IndexPage",
  setup() {
    const eventsFromServer = ref([
      // { data: 'hii', time: '32234' },
      // { data: 'hii324', time: '3223422' },
    ]);
    const serverUrl =
      process.env.NODE_ENV === "production"
        ? "YOUR_WEBSOCKET_URL"
        : "ws://localhost:8000/events";

    const socket = new WebSocket(serverUrl);
    socket.addEventListener("open", (event) => {
      console.log("Connected to server");
    });

    socket.addEventListener("message", function (event) {
      console.log("Message from server ", event.data);
      eventsFromServer.value.push({ time: new Date(), data: event.data });
    });

    return { eventsFromServer };
  },
  methods: {
    register() {
      this.$router.push("/register");
    },
  },
});
</script>

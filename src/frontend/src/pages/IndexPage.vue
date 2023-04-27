<template>
  <q-page class="bg-grey-10">
    <div class="row fixed-center">
      <!-- <div class="col">
        <q-avatar class="self-center" size="16em">
          <img src="https://cdn.quasar.dev/img/avatar.png">
        </q-avatar>
      </div> -->
      <div class="col column">
        <q-avatar size="16em">
          <img src="https://cdn.quasar.dev/img/avatar.png">
        </q-avatar>
        <h4 class="q-mt-sm self-center text-white">UserName</h4>
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
});
</script>

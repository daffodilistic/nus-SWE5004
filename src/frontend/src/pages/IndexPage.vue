<template>
  <q-page>
    <div class="q-pa-md">
      <div class="row flex flex-center">
        <!-- <div class="col flex flex-center">
          <q-card class="user-profile fit">
            <q-img src="https://cdn.quasar.dev/img/parallax2.jpg">
              <div class="absolute-bottom text-subtitle2 text-center">
                Title
              </div>
            </q-img>
          </q-card>
        </div> -->
        <div>
          <q-btn outline color="primary" label="Add New User" />
        </div>
        <div>
          <button @click="connect()">Connect</button>
          <button @click="disconnect()">Disconnect</button>
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

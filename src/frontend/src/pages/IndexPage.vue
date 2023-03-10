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
import { defineComponent } from "vue";

export default defineComponent({
  name: "IndexPage",
});
</script>

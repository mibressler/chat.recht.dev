<template>
  <v-app id="inspire">
    <v-system-bar app>
      
    </v-system-bar>

    <v-app-bar
      app
      clipped-right
      flat
      height="72"
    >
      <v-spacer></v-spacer>


    </v-app-bar>

  

    <v-main>
      <!--  -->
    </v-main>

    <v-footer
      app
      color="transparent"
      height="72"
      inset
    >
    <div class="center" style="width:600px;">
      <v-text-field
        background-color="grey lighten-1"
        dense
        flat
        hide-details
        rounded
        solo
      ></v-text-field>
        <v-form>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="message"
            :append-icon="marker ? 'mdi-map-marker' : 'mdi-map-marker-off'"
            :append-outer-icon="message ? 'mdi-send' : 'mdi-microphone'"
            :prepend-icon="icon"
            filled
            clear-icon="mdi-close-circle"
            clearable
            label="Message"
            type="text"
            @click:append="toggleMarker"
            @click:append-outer="sendMessage"
            @click:prepend="changeIcon"
            @click:clear="clearMessage"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
    </div>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    data: () => ({ drawer: null }),
  }
</script>

<style scoped>
.center {
  margin: auto;
}
</style>
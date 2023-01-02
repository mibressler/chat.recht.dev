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
      height="220"
      inset
    >
    <div class="center" style="width:600px;">
        <v-form>
    <v-container>
      <v-row>
        <v-col cols="12">
<v-combobox
          v-model="select"
          :items="items"
          label="Funktionalität"
        ></v-combobox>
          <v-text-field
            v-model="message"
            :append-outer-icon="message ? 'mdi-send' : 'mdi-send'"
            filled
            clear-icon="mdi-close-circle"
            clearable
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
    data: () => ({
      password: 'Password',
      show: false,
      marker: true,
      iconIndex: 0,
      icons: [
        'mdi-emoticon',
        'mdi-emoticon-cool',
        'mdi-emoticon-dead',
        'mdi-emoticon-excited',
        'mdi-emoticon-happy',
        'mdi-emoticon-neutral',
        'mdi-emoticon-sad',
        'mdi-emoticon-tongue',
      ],
      select: ['Verwandte Urteile'],
        items: [
          'Verwandte Urteile',
          'Fallbearbeitung',
        ],
    }),

    computed: {
      icon () {
        return this.icons[this.iconIndex]
      },
    },

    methods: {
      toggleMarker () {
        this.marker = !this.marker
      },
      sendMessage () {
        this.resetIcon()
        this.clearMessage()
      },
      clearMessage () {
        this.message = ''
      },
      resetIcon () {
        this.iconIndex = 0
      },
      changeIcon () {
        this.iconIndex === this.icons.length - 1
          ? this.iconIndex = 0
          : this.iconIndex++
      },
    },
  }
</script>

<style scoped>
.center {
  margin: auto;
}
</style>
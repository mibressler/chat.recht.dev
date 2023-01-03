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
          <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <div class="pr-5">
        <v-btn
          v-bind="attrs"
          v-on="on"
          icon
        
        >
          <v-icon>mdi-information-outline</v-icon>
        </v-btn></div>
      </template>
      <v-card>
        <v-toolbar
          dark
          color="white"
          elevation="0"
        >
          
         
          <v-spacer></v-spacer>
          <v-toolbar-items>
              <v-btn
            icon
            color="grey"
            @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          </v-toolbar-items>
        </v-toolbar>
       
      </v-card>
    </v-dialog>

    </v-app-bar>

  

    <v-main>
      <!--  -->
<div class="center mt-10" style="width:700px;">
      <v-card
                v-for="(video, i) in treffer"
                :key="i"
                class="elevation-0 pt-1 pb-2"
                max-height="200"
                
              >
    <div class="d-flex flex-no-wrap">

      

<v-img
      v-if="hover"
      class="white--text align-end"
      max-height="138px"
      max-width="245px"
      src="https://www.onlinesolutionsgroup.de/wp-content/uploads/giphy.gif"
    >
      <v-card-text align="right" class="pb-1 pr-2"><div style="elevation-24">{{ video.duration }}</div></v-card-text>
    </v-img>

   
    <v-img
      v-else
      src="https://www.tum-cdps.de/wp-content/uploads/lecturehall.jpg"
      class="white--text align-end"
      max-height="138px"
      max-width="245px"
    >
      <v-card-text align="right" class="pb-1 pr-2"><div style="elevation-24"></div></v-card-text>
    </v-img>

    <div>
      <v-card-text style="font-size:1.2em; font-weight:400;" class="pt-2 pb-1">{{ video.metadata.court.name }}</v-card-text>
    <v-card-subtitle class="pb-2 pt-0">
      {{ video.score }} {{ video.metadata.date }}
    </v-card-subtitle>
    <v-card-text class="text--primary">
      <div>{{ video.summary }}</div><div class="mt-2">


        

      
      
      
      </div>
    </v-card-text>
    </div>
    </div>
  </v-card>
  </div>
      
    </v-main>

    <v-footer
      app
      color="white"
      height="220"
      inset
    >
    <div class="center" style="width:700px;">
        <v-form>
    <v-container>
      <v-row>
        <v-col cols="12">
<v-combobox
          v-model="select"
          :items="items"
          label="Auswählen"
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
import axios from 'axios'
export default {
    data: () => ({
      dialog: false,
      treffer: [],
      message: [],
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
      select: ['Urteile suchen'],
        items: [
          'Urteile suchen',
          'Fallbearbeitung für diesen Fall',
        ],
         vorlesungen: [
        {
          title: 'Familienrecht',
          subtitle: '',
          date: '3 CN 2/21 vom 25.10.2022',
          description: 'Für den Termin zur Verkündung einer Entscheidung am 22. November 2022 werden Ton- und Fernseh-Rundfunkaufnahmen zum Zwecke der Veröffentlichung ihres Inhalts zugelassen.',
          duration: '1:30:00',
          type: 'Vorlesung',
          image: 'https://www.tum-cdps.de/wp-content/uploads/lecturehall.jpg',
          file: 'https://www.tum-cdps.de/wp-content/uploads/VL1.pdf',
          disabled: false,
          location: "Hörsaal 2370",
        },
        {
          title: 'Verwaltungsrecht',
          subtitle: '',
          date: '3 CN 2/21 vom 25.10.2022',
          description: 'Die Fernseh-Rundfunkaufnahmen dürfen nur mit ortsfesten Kameras an den dafür im Sitzungssaal vorgesehenen Standplätzen gemacht werden.',
          duration: '1:30:00',
          type: 'Vorlesung',
          image: 'https://www.tum-cdps.de/wp-content/uploads/lecturehall.jpg',
          disabled: false,
          file: 'https://www.tum-cdps.de/wp-content/uploads/VL2.pdf',
          location: "Hörsaal 2370",
        },
         ]
    }),
    computed: {
      icon () {
        return this.icons[this.iconIndex]
      },
      prompt () {
        return this.message
      },
    },

    methods: {
      toggleMarker () {
        this.marker = !this.marker
      },
      sendMessage () {
        this.makeRequest()
        
      },
      makeRequest () {
        axios
            .get('https://api.recht.dev/reference?prompt='+this.message)
            .then((response) => {
                  this.treffer = response.data.data
                })

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
    mounted() {
    axios
      .get('http://localhost:8082/api/inhalte?populate=*')
      .then((response) => {
        this.announcements = response.data.data
      })
  }
}
</script>

<style scoped>
.center {
  margin: auto;
}
</style>
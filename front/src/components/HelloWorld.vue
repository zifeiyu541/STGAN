<template>
  <div class="hello">
    <div class="select_pid">
      <input v-model="pid">
      <button @click="refresh()">refresh</button>
      <br>
      <button @click="prev()">prev</button>
      <button @click="next()">next</button>
      <button @click="random()">random</button>
    </div>

    <div class="select_att">
      <input type="radio" id="Bald" value="Bald" v-model="attribute">
      <label for="Bald">Bald</label>
      <input type="radio" id="Bangs" value="Bangs" v-model="attribute">
      <label for="Bangs">Bangs</label>
      <input type="radio" id="Black_Hair" value="Black_Hair" v-model="attribute">
      <label for="Black_Hair">Black_Hair</label>
      <input type="radio" id="Blond_Hair" value="Blond_Hair" v-model="attribute">
      <label for="Blond_Hair">Blond_Hair</label>
      <input type="radio" id="Brown_Hair" value="Brown_Hair" v-model="attribute">
      <label for="Brown_Hair">Brown_Hair</label>
      <input type="radio" id="Bushy_Eyebrows" value="Bushy_Eyebrows" v-model="attribute">
      <label for="Bushy_Eyebrows">Bushy_Eyebrows</label>
      <input type="radio" id="Eyeglasses" value="Eyeglasses" v-model="attribute">
      <label for="Eyeglasses">Eyeglasses</label>
      <br>
      <input type="radio" id="Male" value="Male" v-model="attribute">
      <label for="Male">Male</label>
      <input type="radio" id="Mouth_Slightly_Open" value="Mouth_Slightly_Open" v-model="attribute">
      <label for="Mouth_Slightly_Open">Mouth_Slightly_Open</label>
      <input type="radio" id="Mustache" value="Mustache" v-model="attribute">
      <label for="Mustache">Mustache</label>
      <input type="radio" id="No_Beard" value="No_Beard" v-model="attribute">
      <label for="No_Beard">No_Beard</label>
      <input type="radio" id="Pale_Skin" value="Pale_Skin" v-model="attribute">
      <label for="Pale_Skin">Pale_Skin</label>
      <input type="radio" id="Young" value="Young" v-model="attribute">
      <label for="Young">Young</label>
      <br>
    </div>

    <span>
      <img :src=img_raw />
      <br>
      raw_image
    </span>
    <span>
      <img :src=img_att />
      <br>
      {{ attribute }}: {{ flag }}
    </span>
  </div>
</template>

<script>
import axios from 'axios'

let img_path = 'output/128/sample_testing/'

export default {
  name: 'HelloWorld',
  data () {
    return {
      pid: '100000',
      attribute: 'Bald',
      img_raw: img_path + "100000_raw.png",
      img_att: img_path + "100000_Bald.png",
      flag: "++"
    }
  },
  methods:{
    random() {
      this.pid = Math.round(Math.random() * 100000 + 100000);
    },
    prev() {
      if(this.pid > 100000) {
        this.pid--;
      }
    },
    next() {
      if(this.pid < 200000) {
        this.pid++;
      }
    },
    refresh() {
      axios({
        method: 'GET',
        url: 'http://localhost:1234/getPicture',
        params: {
          pid: this.pid,
          attribute: 'raw'
        }
      }).then((response) => {
        console.log(response);
        if(response.data === "unavailable attribute") {
          alert("属性错误")
        }
        this.img_raw = img_path + response.data;

        axios({
          method: 'GET',
          url: 'http://localhost:1234/getPicture',
          params: {
            pid: this.pid,
            attribute: this.attribute
          }
        }).then((response) => {
          console.log(response);
          if(response.data === "unavailable attribute") {
            alert("属性错误")
          }
          let args = response.data.split('$')
          this.img_att = img_path + args[0]
          if(args[1] === '1') {
            this.flag = "--"
          } else {
            this.flag = "++"
          }
        })
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

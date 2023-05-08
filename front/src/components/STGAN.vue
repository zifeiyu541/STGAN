<template>
  <div class="app">
    <div class="header">
      <span>基于STGAN的人脸图像任意属性编辑系统</span>
    </div>
    <div class="content">
      <div class="aside">
        <div class="img">
          <el-image
              style="width: 256px; height: 256px"
              fit="fill"
              :src=img_raw
              v-loading="loading"
          >
          </el-image>
          <span>原图片</span>
        </div>
      </div>
      <div class="main">
        <el-card class="card">
          <div class="file">
            <span>请输入图片编号</span>
            <div class="fileInput">
              <el-input-number v-model="pid" :min="100000" :max="200000"
                               label="请输入图片编号" @change="refresh"/>
              <el-button type="success" plain @click="random">Random</el-button>
            </div>
          </div>
          <div class="file">
            <span>请输入图片路径（图片格式须为jpg）</span>
            <div class="fileInput">
              <el-input
                  v-model="url"
                  :rows="3"
                  type="textarea"
                  placeholder="Please input the URL of the image"
              />
              <el-button  type="primary" plain @click="generate">Generate</el-button>
            </div>
          </div>
          <div class="file">
            <div class="fileInput">
              <span>请上传本地图片（图片格式须为jpg）</span>
              <el-upload
                  ref="upload"
                  class="upload-demo"
                  action="http://localhost:1234/uploadPicture"
                  :show-file-list=false
                  :limit="1"
                  :on-success="handleSuccess"
                  :before-upload="handleBefore"
                  >
                <el-button type="primary">upload</el-button>
              </el-upload>
            </div>
          </div>
          <div class="type">
            <span>请选择应用效果</span>
            <el-select v-model="attribute" placeholder="请选择效果" @change="refresh">
              <el-option
                  v-for="type in types"
                  :key="type"
                  :label="type"
                  :value="type"
              ></el-option>
            </el-select>
          </div>
        </el-card>
      </div>
      <div class="aside">
        <div class="img">
          <el-image
              style="width: 256px; height: 256px"
              fit="fill"
              :src=img_att
              v-loading="loading"
          >
          </el-image>
          <span>{{ attribute }} {{ flag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'STGAN',
  data () {
    return {
      pid: 100000,
      attribute: 'Bald',
      types: ['Bald', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Bushy_Eyebrows',
        'Eyeglasses', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'No_Beard', 'Pale_Skin', 'Young'],
      img_raw: "",
      img_att: "",
      flag: "++",
      url: "",
      loading: false,
      fileList: []
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    random() {
      this.pid = Math.round(Math.random() * 100000 + 100000);
      this.refresh();
    },
    handleBefore() {
      this.loading = true
    },
    handleSuccess(response) {
      console.log(response)
      // 清空已上传的图片
      let uploadInstance = this.$refs.upload
      uploadInstance.clearFiles()
      if(response === "success") {
        this.pid = 200000
        this.refresh()
      } else {
        alert("图片上传失败")
        this.loading = false
      }
    },
    generate() {
      this.loading = true
      axios({
        method: 'GET',
        url: 'http://localhost:1234/getPictureByUrl',
        params: {
          url: this.url
        }
      }).then((response) => {
        console.log(response);
        if(response.data === "success") {
          this.pid = 200000
          this.refresh()
        } else {
          alert("图片获取失败")
          this.loading = false
        }
      })
    },
    refresh() {
      this.loading = true
      axios({
        method: 'GET',
        url: 'http://localhost:1234/getPicture',
        responseType: "arraybuffer",
        params: {
          pid: this.pid,
          attribute: 'raw'
        }
      }).then((response) => {
        console.log(response);
        if(response.data === "unavailable attribute") {
          alert("属性错误")
        }
        const data = String.fromCharCode.apply(null, new Uint8Array(response.data))
        if(data === "generation failed") {
          alert("图片生成失败，请使用jpg图片")
          this.loading = false
          return
        }
        // this.img_raw = img_path + response.data;
        const blob = new Blob([response.data], { type: 'image/png' })  // 将二进制数据转换为 Blob 对象
        this.img_raw = URL.createObjectURL(blob)  // 创建图片 URL
        // 将 imgUrl 显示在页面上

        axios({
          method: 'GET',
          url: 'http://localhost:1234/getPicture',
          responseType: "arraybuffer",
          params: {
            pid: this.pid,
            attribute: this.attribute
          }
        }).then((response) => {
          console.log(response);
          if(response.data === "unavailable attribute") {
            alert("属性错误")
          }
          const blob = new Blob([response.data], { type: 'image/png' })  // 将二进制数据转换为 Blob 对象
          this.img_att = URL.createObjectURL(blob)  // 创建图片 URL

          axios({
            method: 'GET',
            url: 'http://localhost:1234/getPictureFlag',
            params: {
              pid: this.pid,
              attribute: this.attribute
            }
          }).then((response) => {
            console.log(response);
            if(response.data === 1) {
              this.flag = "--"
            } else {
              this.flag = "++"
            }
            this.loading = false
          })

          // let args = response.data.split('$')
          // this.img_att = img_path + args[0]
          // if(args[1] === '1') {
          //   this.flag = "--"
          // } else {
          //   this.flag = "++"
          // }
        })
      })
    }
  }
}
</script>

<style scoped>
html, body, .app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: aliceblue;
}
.header {
  width: 100%;
  height: 15%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  background-color: lightblue;
}
.header > span {
  font-weight: bold;
  font-size: x-large;
}
.content {
  width: 100%;
  height: 85%;
  display: flex;
  justify-content: space-between;
}
.aside {
  height: 100%;
  width: 30%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
.aside span {
  font-weight: bold;
}
.main {
  height: 100%;
  width: 40%;
}
.img {
  width: 80%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
.card {
  width: 100%;
  height: 75%;
  margin-top: 10%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.file {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  margin-bottom: 10px;
}
.file > span {
  font-weight: bold;
  color: grey;
  margin-bottom: 10px;
}
.fileInput {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.fileInput > span {
  font-weight: bold;
  color: grey;
}
.type {
  display: flex;
  flex-direction: column;
}
.type > span {
  font-weight: bold;
  color: grey;
  margin-bottom: 10px;
}
</style>

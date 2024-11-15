<script setup lang="ts">
import { ref } from 'vue'

import Crypt from './Crypt.vue';
import Decrypt from './Decrypt.vue';

defineProps({
  msg: String,
})

const tab = ref("crypt")
const count = ref(0)
const cryptographySelector = ref("encrypt")
const product = ref(null);

interface User {
  name: string
  imageUrl: string
}

const users: Array<User> = [
  {
    "name": "Reven Ferlian",
    "imageUrl": "https://kuliah.unsia.ac.id/assets/img/default-male.svg",
  },
  {
    "name": "SEDRY MUHAMMAD IQBAL",
    "imageUrl": "https://kuliah.unsia.ac.id/assets/img/default-male.svg",
  },
  {
    "name": "SAMAN FATRIANSYAH",
    "imageUrl": "https://storage.googleapis.com/assets-edlink/p/thumb-b237e3239e90450c5496572ae076232a50b04760a43396478094dbfa8c81f648-foto-dasi.jpg",
  },
  {
    "name": "ROYYAN MUSTAWAN",
    "imageUrl": "https://kuliah.unsia.ac.id/assets/img/default-male.svg",
  },
  {
    "name": "RIZKI HIKMAWAN",
    "imageUrl": "https://kuliah.unsia.ac.id/assets/img/default-male.svg",
  },
  {
    "name": "RISFANDI BAYUNDA RAMADHAN",
    "imageUrl": "https://kuliah.unsia.ac.id/assets/img/default-male.svg",
  },
  {
    "name": "RICKY BACHTIAR",
    "imageUrl": "https://storage.googleapis.com/assets-edlink/p/thumb-cf12e3c948c5ce16b06fcbe24de2b6d647d7394a40833aee8a4b0a21b1afd57a-img-20201216-114337.jpg",
  },
]

const onCrypt = () => {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ method: 'sha', value: "test" })
  };

  fetch('http://127.0.0.1:5000/crypt', requestOptions)
    .then(response => response.json())
    .then(data => product.value = data);
}

const onDecrypt = () => {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ method: 'sha', value: "testx", decrypt_key: "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" })
  };

  fetch('http://127.0.0.1:5000/decrypt', requestOptions)
    .then(response => response.json())
    .then(data => product.value = data);
}
</script>

<template>

  <div role="tablist" class="tabs tabs-boxed">
    <a role="tab" class="tab" :class="{ 'tab-active': tab == 'crypt' }" @click="tab = 'crypt'">Crypt</a>
    <a role="tab" class="tab" :class="{ 'tab-active': tab == 'decrypt' }" @click="tab = 'decrypt'">Decrypt</a>
  </div>

  <Crypt v-if="tab == 'crypt'" />
  <Decrypt v-else />

  <!-- <h1>{{ msg }}</h1>
  <button
    class="inline-block cursor-pointer rounded-md bg-gray-800 px-4 py-3 text-center text-sm font-semibold uppercase text-white transition duration-200 ease-in-out hover:bg-gray-900">
    Button
  </button>
  <div class="card">
    <select name="cryptography-selector" id="cryptography-selector" v-model="cryptographySelector">
      <option value="encrypt">encrypt</option>
      <option value="decrypt">decrypt</option>
    </select>

    <input type="text" v-show="cryptographySelector == 'encrypt'">
    <input type="text" v-show="cryptographySelector == 'decrypt'">
    <input type="text" v-show="cryptographySelector == 'decrypt'">
  </div>

  {{ product?.res }}

  <div class="card">
    <button type="button" @click="onCrypt()">Crypt</button>
    <button type="button" @click="onDecrypt()">onDecrypt</button>

    <button type="button" @click="count++">count is {{ count }}</button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank">create-vue</a>, the official Vue + Vite
    starter
  </p>
  <p>
    Learn more about IDE Support for Vue in the
    <a href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support" target="_blank">Vue Docs Scaling up
      Guide</a>.
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p> -->
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>

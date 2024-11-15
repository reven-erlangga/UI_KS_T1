<script setup lang="ts">
import { Ref, ref } from 'vue';
import Step from './Step.vue';
import { useBase64 } from '@vueuse/core'

const method = ref('sha')
const encrypted = ref(null)
let hashKey = ref()
const result = ref(null)
const file = ref() as Ref<File>

const { base64: fileBase64 } = useBase64(file)

const onSubmit = () => {
    let requestOptions;
    if (method.value == 'rsa') {
        requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },// @ts-ignore
            body: JSON.stringify({ method: method.value, hash_key: cryptKeyFile.value.split(',')[1], encrypted: messageFile.value.split(',')[1] })
        }
    } else {
        requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ method: method.value, hash_key: hashKey.value, encrypted: encrypted.value })
        }
    }

    fetch('http://127.0.0.1:5000/decrypt', requestOptions)
        .then(response => response.json())
        .then(data => result.value = data)
}

import * as yup from 'yup'
import { useField, useForm } from 'vee-validate'

const { errors, defineField, handleSubmit } = useForm({
    validationSchema: yup.object({
        cryptKeyFile: yup.string(),
        messageFile: yup.string(),
    }),
});

const { value: cryptKeyFile, errorMessage: cryptKeyFileErrorMessage } = useField('cryptKeyFile');
const { value: messageFile, errorMessage: messageFileErrorMessage } = useField('messageFile');

function onCryptKeyFileChanged($event: Event) {
    const target = $event.target as HTMLInputElement;
    if (target && target.files) {
        const file = target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function () {
            cryptKeyFile.value = reader.result
        };
    }
}

function onMessageFileChanged($event: Event) {
    const target = $event.target as HTMLInputElement;
    if (target && target.files) {
        const file = target.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function () {
            messageFile.value = reader.result
        };
    }
}

const getDataPart = (dataUrl) => dataUrl.split(',')[1];
</script>

<template>
    {{ file }}
    <div class="w-[30rem] my-4">
        <form v-if="!result" @submit.prevent="onSubmit" enctype="multipart/form-data" class="grid grid-cols-1 gap-4">
            <div class="grid grid-cols-1 gap-4">
                <select class="select select-bordered" v-model="method">
                    <option value="sha">Hashing (SHA)</option>
                    <option value="aes">Symmetric (AES)</option>
                    <option value="rsa">Asymmetric (RSA)</option>
                </select>

                <div v-if="method == 'rsa'" class="grid grid-cols-2 gap-4">
                    <div class="flex flex-wrap flex-col gap-2 items-start">
                        <label for="">Crypt Key File</label>
                        <input type="file" class="file-input file-input-bordered file-input-accent  w-full max-w-xs"
                            placeholder="Insert encryption file" @change="onCryptKeyFileChanged" />
                    </div>

                    <div class="flex flex-wrap flex-col gap-2 items-start">
                        <label for="">Message File</label>
                        <input type="file" class="file-input file-input-bordered file-input-info w-full max-w-xs"
                            @change="onMessageFileChanged" />
                    </div>
                </div>

                <div v-else class="flex flex-col gap-4">
                    <input class="input input-bordered join-item w-full"
                        :placeholder="method == 'sha' ? 'original value' : 'hashing key'" v-model="hashKey" />

                    <input class="input input-bordered join-item w-full" placeholder="encrypted value"
                        v-model="encrypted" />
                </div>

            </div>

            <button type="submit" class="btn btn-block btn-primary">Decrypt</button>
        </form>

        <button v-if="result" class="btn btn-block btn-outline btn-secondary" @click="result = null">Reset</button>

        <Step v-if="result?.data" :data="result.data" class="mt-10" />
    </div>
</template>
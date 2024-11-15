<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Step from './Step.vue';
import { Form, useField } from 'vee-validate'
import * as yup from 'yup'
import { useForm } from 'vee-validate'

const result = ref(null)

const { errors, defineField, defineInputBinds, setFieldValue, handleSubmit } = useForm({
    validationSchema: yup.object({
        method: yup.string().required().default("sha"),
        cryptKey: yup.string().min(8),
        word: yup.string().required('Please insert word to encrypt'),
    }),
});

const method = defineInputBinds('method')
const cryptKey = defineInputBinds('cryptKey')
const word = defineInputBinds('word')

const onSubmit = handleSubmit(values => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method: values.method, value: values.word, crypt_key: values.cryptKey })
    }

    fetch('http://127.0.0.1:5000/crypt', requestOptions)
        .then(response => response.json())
        .then(data => result.value = data)
})

onMounted(() => {
    setFieldValue("method", "sha")
})
</script>

<template>
    <div class="w-[30rem] my-4">
        <form v-if="!result" @submit.prevent="onSubmit" class="grid grid-cols-1 gap-4">
            <div class="join">
                <select class="select select-bordered join-item" v-bind="method"
                    :class="errors.cryptKey?.length > 0 ? 'select-error' : ''">
                    <option value="sha">Hashing (SHA)</option>
                    <option value="aes">Symmetric (AES)</option>
                    <option value="rsa">Asymmetric (RSA)</option>
                </select>

                <input class="input input-bordered join-item w-full"
                    :class="errors.cryptKey?.length > 0 ? 'select-error' : ''"
                    placeholder="write something to encryption..." v-bind="word" />
            </div>

            <input v-if="method.value == 'aes'" class="input input-bordered join-item w-full"
                :class="errors.cryptKey?.length > 0 ? 'input-error' : ''" placeholder="encryption key"
                v-bind="cryptKey" />

            <div v-if="errors.cryptKey" role="alert" class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span v-text="errors.cryptKey"></span>
            </div>

            <button type="submit" class="btn btn-block btn-primary" :disabled="method == null">Crypt</button>
        </form>

        <button v-if="result" class="btn btn-block btn-outline btn-secondary" @click="result = null">Reset</button>

        <Step v-if="result?.data" :data="result.data" class="mt-10" />
    </div>
</template>
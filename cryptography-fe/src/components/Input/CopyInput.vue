<script setup lang="ts">
import { ref } from 'vue';
import ContentCopyIcon from 'vue-material-design-icons/ContentCopy.vue';

const props = defineProps({
    value: { type: String, required: true },
})

const elementVisible = ref(false);

function copyToClipboard() {
    var audio = new Audio('copy.wav')
    audio.play();


    elementVisible.value = true
    navigator.clipboard.writeText(props.value);
    setTimeout(() => elementVisible.value = false, 1000)
}
</script>

<template>
    <div class="join"><input class="input w-full join-item" :value="value" disabled />
        <button class="btn join-item rounded-r-full" @click="copyToClipboard">
            <h1 v-if="elementVisible" v-show="elementVisible" class="hideElement"> Copied! </h1>
            <ContentCopyIcon v-else />
        </button>
    </div>
</template>
<script setup lang="ts">
interface Step {
    title: string
    description: string
    items: any
}

defineProps({
    data: Array<Step>,
})

import CopyInput from './Input/CopyInput.vue';
</script>

<template>
    <ul class="timeline timeline-snap-icon max-md:timeline-compact timeline-vertical w-full">
        <li v-for="(step, index) in data">
            <div class="timeline-middle">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                    class="text-primary h-5 w-5">
                    <path fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                        clip-rule="evenodd" />
                </svg>
            </div>

            <div class="mb-10" :class="index % 2 == 0 ? 'timeline-start md:text-end' : 'timeline-end md:text-start'">
                <span class="font-mono italic" v-text="step.title"></span>
                <div v-if="step.items" v-for="(item, index) in step.items">
                    <div class="text-md" v-text="step.description?.replace('[' + index + ']', '')"></div>
                    <span v-if="step.description.indexOf(index)">
                        <CopyInput v-if="item.type == 'input'" :value="item.value" class="mt-3" />
                        <a v-else-if="item.type == 'link'" :href="item.value" class="mt-3 link link-accent">Download</a>
                    </span>
                </div>
                <div v-else class="text-md" v-text="step.description"></div>
            </div>

            <hr v-if="index != Object.keys(data).length - 1" class="bg-primary" />
        </li>
    </ul>
</template>
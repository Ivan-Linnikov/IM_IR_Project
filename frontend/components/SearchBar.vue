<template>
    <div class="flex flex-col items-center justify-center">
        <div class="font-raleway text-[#111111]">
            <form ref="searchForm"
                class="flex items-center w-full max-w-5xl bg-white rounded-full shadow-lg p-4 space-x-4"
                @submit.prevent="performSearch">

                <!-- Search Input -->
                <div class="flex items-center space-x-2 ">
                    <Icon icon="mdi:magnify" class="h-5 w-5 " />
                    <input type="query" v-model="searchQuery" placeholder="Type what you need ..."
                        class="outline-none bg-white text-black  placeholder-[#111111] w-52 " required />
                </div>

                <!-- Location -->
                <div class="flex items-center border-l pl-4 space-x-2">
                    <Icon icon="mdi:map-marker" class="h-5 w-5 " />
                    <input type="text" v-model="location" placeholder="Where you are ..."
                        class="outline-none bg-white text-black w-52 placeholder-[#111111] " />
                </div>

                <!-- Date -->
                <div class="flex items-center border-l pl-4 space-x-2 cursor-pointer" @click="openDatePicker">
                    <Icon icon="mdi:calendar-outline" class="h-5 w-5  cursor-pointer" />
                    <input type="date" ref="dateInput" v-model="date"
                        class="bg-white outline-none cursor-pointer placeholder-[#111111] " />
                </div>

                <!-- Time -->
                <div class="flex items-center border-l pl-4 space-x-2 cursor-pointer" @click="openTimePicker">
                    <Icon icon="mdi:clock-outline" class="h-5 w-5  cursor-pointer" />
                    <input type="time" ref="timeInput" v-model="time"
                        class="bg-white outline-none  cursor-pointer placeholder-[#111111] " />
                </div>

                <!-- Search Button -->
                <button type="submit"
                    class="ml-auto bg-black text-white px-6 py-2 rounded-full transition-all duration-300 hover:border hover:border-black hover:bg-white hover:text-[#111111] ">
                    Search
                </button>
            </form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Icon } from '@iconify/vue';
import { useRouter } from 'vue-router';
import { useSearchStore } from '~/stores/searchStore';
import { ref } from 'vue';

const store = useSearchStore();
const router = useRouter();

const searchQuery = ref<string>('');
const location = ref<string>('');
const date = ref<string>('');
const time = ref<string>('');

const dateInput = ref<HTMLInputElement | null>(null);
const timeInput = ref<HTMLInputElement | null>(null);

const openDatePicker = () => {
    if (dateInput.value) {
        dateInput.value.showPicker ? dateInput.value.showPicker() : dateInput.value.click();
    }
};

const openTimePicker = () => {
    if (timeInput.value) {
        timeInput.value.showPicker ? timeInput.value.showPicker() : timeInput.value.click();
    }
};

const performSearch = async () => {
    try {
        store.setSearchData(searchQuery.value, location.value, date.value, time.value);
        
        router.push('/result');
    } catch (err) {
        console.error('Search error:', err instanceof Error ? err.message : String(err));
    }
};







</script>

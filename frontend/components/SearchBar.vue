<template>
    <div class="flex flex-col items-center justify-center">
        <div class="font-raleway text-[#111111]">
            <form ref="searchForm"
                class="flex items-center w-full max-w-5xl bg-white rounded-full shadow-lg p-4 space-x-4"
                @submit.prevent="performSearch">

                <!-- Search Input -->
                <div class="flex items-center space-x-2 ">
                    <Icon icon="mdi:magnify" class="h-5 w-5 " />
                    <input type="text" v-model="searchQuery" placeholder="Type what you need ..."
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

<script setup>
import { Icon } from '@iconify/vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // Use router for navigation

// Form inputs
const searchQuery = ref('');
const location = ref('');
const date = ref('');
const time = ref('');

// Form reference
const searchForm = ref(null);

// Date and time inputs
const dateInput = ref(null);
const timeInput = ref(null);

// Router instance
const router = useRouter();

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

const performSearch = () => {
    // Validate the form using native form validation
    if (!searchForm.value.checkValidity()) {
        console.warn('The form is not valid. Please fill in the required fields.');
        searchForm.value.reportValidity(); // Show native validation message
        return; // Stop execution and prevent redirection
    }

    // Log the input data to the console
    console.log('Search Query:', searchQuery.value);
    console.log('Location:', location.value);
    console.log('Date:', date.value);
    console.log('Time:', time.value);

    // Redirect to the result page
    router.push('/result');
};
</script>
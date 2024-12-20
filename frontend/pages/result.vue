<template>
    <div class="bg-[#f1f1f1] bg-cover min-h-screen font-raleway p-10">
        <!-- Title and Search Bar -->
        <div class="flex flex-column items-center w-full">
            <!-- Title on the very left of the page -->
            <NuxtLink to="/" class="pl-0">
                <h1 class="font-oswald text-4xl text-[#111111] font-normal">Find Beauty</h1>
            </NuxtLink>
            <!-- Centered Search Bar -->
            <div class="flex-grow flex justify-center">
                <SearchBar class="w-full max-w-6xl" />
            </div>
        </div>


        <!-- Filter Section -->
        <div class="flex justify-center mt-8">
            <div class="flex items-end justify-center w-full max-w-6xl space-x-4">

                <!-- City Select -->
                <div class="w-1/3 relative">
                    <label for="city" class="block text-sm font-medium text-[#111111] mb-2">City</label>
                    <div class="flex items-center w-full bg-white rounded-full shadow-lg p-3 space-x-2">
                        <input type="text" v-model="cityInput" @input="filterCities" @focus="showCityOptions = true"
                            @blur="hideOptions" id="city" placeholder="Type or select a city"
                            class="outline-none bg-white text-[#111111] placeholder-[#111111] flex-1 min-w-0" />
                    </div>
                    <ul v-if="showCityOptions && filteredCities.length"
                        class="absolute z-10 bg-white shadow-lg rounded-lg mt-2 max-h-40 overflow-y-auto w-full">
                        <li v-for="(city, index) in filteredCities" :key="index" @mousedown="selectCity(city)"
                            class="p-4 text-[#111111] hover:bg-black hover:text-white cursor-pointer">
                            {{ city }}
                        </li>
                    </ul>
                </div>

                <!-- Day of the Week Select -->
                <div class="w-1/5">
                    <label for="day" class="block text-sm font-medium text-[#111111] mb-2">Day</label>
                    <div class="flex items-center w-full bg-white rounded-full shadow-lg p-3">
                        <select id="day" class="outline-none bg-white text-[#111111] flex-1 min-w-0 appearance-none">
                            <option value="">Select a day</option>
                            <option value="Monday">Monday</option>
                            <option value="Tuesday">Tuesday</option>
                            <option value="Wednesday">Wednesday</option>
                            <option value="Thursday">Thursday</option>
                            <option value="Friday">Friday</option>
                            <option value="Saturday">Saturday</option>
                            <option value="Sunday">Sunday</option>
                        </select>
                    </div>
                </div>

                <!-- Time Input -->
                <div class="w-1/5">
                    <label for="time" class="block text-sm font-medium text-[#111111] mb-2">Time</label>
                    <div class="flex items-center w-full bg-white rounded-full shadow-lg p-3 cursor-pointer"
                        @click="openTimePicker">
                        <input ref="timeInput" type="time" id="time"
                            class="outline-none bg-white text-[#111111] flex-1 min-w-0 cursor-pointer" />
                    </div>
                </div>

                <!-- Filter Button -->
                <div class="flex items-end">
                    <button @click="applyFilters"
                        class="bg-black text-white px-6 py-3 rounded-full transition-all duration-300 hover:border hover:border-black hover:bg-white hover:text-[#111111]">
                        Filter
                    </button>
                </div>

            </div>
        </div>
        <div v-if="!store.isLoading && !store.errorMessage" class="grid grid-cols-2 gap-10 mt-20 items-start">
            <Card v-for="item in store.results" :key="item.docno" :item="item" />
        </div>

    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useSearchStore } from '~/stores/searchStore';
import SearchBar from '~/components/SearchBar.vue';

const store = useSearchStore();

// City input logic
const cityInput: Ref<string> = ref('');
const filteredCities: Ref<string[]> = ref([]);
const showCityOptions: Ref<boolean> = ref(false);

const cityOptions: string[] = [
    'New York',
    'Los Angeles',
    'Chicago',
    'Houston',
    'Miami',
    'San Francisco',
    'Atlanta',
    'Seattle',
    'Boston',
    'San Diego'
];


function filterCities(): void {
    const input = cityInput.value.toLowerCase();
    filteredCities.value = cityOptions.filter(city =>
        city.toLowerCase().includes(input)
    );
}

function selectCity(city: string): void {
    cityInput.value = city;
    showCityOptions.value = false;
}

function hideOptions(): void {
    setTimeout(() => {
        showCityOptions.value = false;
    }, 150);
}

const timeInput: Ref<HTMLInputElement | null> = ref(null);

function openTimePicker(): void {
    if (timeInput.value) {
        timeInput.value.showPicker();
    }
}

async function applyFilters(): Promise<void> {
    const filters = {
        city: cityInput.value,
        day: (document.getElementById('day') as HTMLSelectElement)?.value || '',
        time: timeInput.value?.value || '',
    };

    console.log('Filters applied with:', filters);

    try {
        store.isLoading = true;
        store.errorMessage = '';
        
        const response = await $fetch('http://localhost:8000/result', {
            method: 'POST',
            body: filters,
        });

        store.results = response as any[];

    } catch (error) {
        console.error('Error applying filters:', error);
        store.errorMessage = 'An error occurred while applying filters.';
    } finally {
        store.isLoading = false;
    }
}
</script>

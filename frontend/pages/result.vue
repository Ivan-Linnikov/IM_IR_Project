<template>
    <div class="bg-[#f1f1f1] bg-cover min-h-screen p-10 font-raleway">
        <div class="flex justify-center">
            <div class="flex flex-row max-w-6xl pt-4">
                <NuxtLink to="/">
                    <h1 class="font-oswald text-4xl text-[#111111] font-normal">Blyat naydi usge chto to</h1>
                </NuxtLink>
                <SearchBar />
            </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-10 mt-20 items-start">
            <Card v-for="item in processedResults" :key="item.id" :item="item" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

interface SearchResult {
    id: number;
    title: string;
    address: string;
    mobile?: string | null;
    email?: string | null;
    categories?: string[];
    openingTimes?: Record<string, string>;
}

const rawData = [
    {
        id: 1,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser", "Stylist"],
        openingTimes: {
            Monday: "10:00 to 20:00",
            Tuesday: "10:00 to 20:00",
            Wednesday: "10:00 to 20:00",
            Thursday: "10:00 to 20:00",
            Friday: "10:00 to 20:00",
            Saturday: "9:00 to 18:00",
            Sunday: "Closed",
        },
    },
    {
        id: 2,
        title: "Another Business Name Here goes",
        address: "Some Address",
        mobile: null,
        email: null,
        categories: [],
        openingTimes: {
            Monday: "9:00 to 19:00",
            Tuesday: "9:00 to 19:00",
            Wednesday: "9:00 to 19:00",
            Thursday: "9:00 to 19:00",
            Friday: "9:00 to 19:00",
            Saturday: "9:00 to 17:00",
            Sunday: "Closed",
        },
    },
    {
        id: 3,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser", "Stylist", "Hairdresser", "Stylist", "Hairdresser", "Stylist", "Hairdresser", "Stylist"],
        openingTimes: {
            Monday: "10:00 to 20:00",
            Tuesday: "10:00 to 20:00",
            Wednesday: "10:00 to 20:00",
            Thursday: "10:00 to 20:00",
            Friday: "10:00 to 20:00",
            Saturday: "9:00 to 18:00",
            Sunday: "Closed",
        },
    },
    {
        id: 4,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser", "Stylist"],
        openingTimes: {
            Monday: "10:00 to 20:00",
            Tuesday: "10:00 to 20:00",
            Wednesday: "10:00 to 20:00",
            Thursday: "10:00 to 20:00",
            Friday: "10:00 to 20:00",
            Saturday: "9:00 to 18:00",
            Sunday: "Closed",
        },
    },
    {
        id: 5,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser", "Stylist"],
        openingTimes: {
            Monday: "10:00 to 20:00",
            Tuesday: "10:00 to 20:00",
            Wednesday: "10:00 to 20:00",
            Thursday: "10:00 to 20:00",
            Friday: "10:00 to 20:00",
            Saturday: "9:00 to 18:00",
            Sunday: "Closed",
        },
    },
    {
        id: 6,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser", "Stylist"],
        openingTimes: {
            Monday: "10:00 to 20:00",
            Tuesday: "10:00 to 20:00",
            Wednesday: "10:00 to 20:00",
            Thursday: "10:00 to 20:00",
            Friday: "10:00 to 20:00",
            Saturday: "9:00 to 18:00",
            Sunday: "Closed",
        },
    },
    {
        id: 7,
        title: "Q-Quality Coiffure",
        address: "Vordergasse 64, 8200 Schaffhausen",
        mobile: "052 625 03 90",
        email: "mail@quu.ch",
        categories: ["Hairdresser"],
    },
];

const processedResults = ref<SearchResult[]>(rawData);
</script>
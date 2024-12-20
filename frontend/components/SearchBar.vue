<template>
    <div class="flex flex-col items-center font-raleway text-[#111111] w-full">
        <form ref="searchForm" class="flex items-center w-full bg-white rounded-full shadow-lg p-4 space-x-4"
            @submit.prevent="performSearch">

            <!-- Search Input -->
            <div class="flex items-center space-x-2 flex-1">
                <Icon icon="mdi:magnify" class="h-5 w-5 text-[#111111]" />
                <input type="query" v-model="searchQuery" placeholder="Type what you need ..."
                    class="outline-none bg-white text-black placeholder-[#111111] flex-1 min-w-0" required />
            </div>

            <!-- Search Button -->
            <button type="submit"
                class="bg-black text-white px-8 py-3 rounded-full transition-all duration-300 hover:border hover:border-black hover:bg-white hover:text-[#111111]">
                Search
            </button>
        </form>
    </div>
</template>


<script lang="ts" setup>
import { Icon } from '@iconify/vue';
import { useSearchStore } from '~/stores/searchStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useSearchStore();

const searchQuery = ref(store.searchQuery);

const performSearch = async () => {
    store.setSearchData(searchQuery.value);

    // Fetch the results regardless of the page
    await store.fetchResults();

    if (router.currentRoute.value.path !== '/result') {
        router.push('/result');
    }
};
</script>
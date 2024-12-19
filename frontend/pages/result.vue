<template>
    <div class="bg-[#f1f1f1] bg-cover min-h-screen p-10 font-raleway">
        <div class="flex justify-center">
            <div class="flex flex-row max-w-6xl pl-4">
                <NuxtLink to="/">
                    <h1 class="font-oswald text-4xl text-[#111111] font-normal pl-4">Find Beauty</h1>
                </NuxtLink>
                <SearchBar />
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center mt-20">
            <p class="text-xl font-bold">Loading results...</p>
        </div>

        <!-- Error State -->
        <div v-if="errorMessage" class="flex justify-center items-center mt-20">
            <p class="text-red-500 text-xl font-bold">{{ errorMessage }}</p>
        </div>

        <!-- Display Results -->
        <div v-if="!isLoading && !errorMessage" class="grid grid-cols-2 gap-10 mt-20 items-start">
            <Card v-for="item in processedResults" :key="item.docno" :item="item" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useSearchStore } from '~/stores/searchStore';
import { useRouter } from 'vue-router';

const store = useSearchStore();


const isLoading = ref<boolean>(true);
const errorMessage = ref<string | null>(null);

const processedResults = computed(() => store.results || []);

const fetchResults = async () => {
    try {
        const response: any = await $fetch('http://localhost:8000', {
            method: 'POST',
            body: { query: store.searchQuery },
        });

        let parsedResponse;
        try {
            parsedResponse = typeof response === 'string' ? JSON.parse(response) : response;
        } catch (err) {
            console.error('Response parsing error', err);
            errorMessage.value = 'Server returned an invalid response.';
            return;
        }

        if (Array.isArray(parsedResponse) && parsedResponse.length > 0) {
            store.setResults(parsedResponse); 
        } else if (Array.isArray(parsedResponse) && parsedResponse.length === 0) {
            errorMessage.value = "No results found for your search.";
        }
        else if (typeof parsedResponse === 'object' && parsedResponse !== null && 'message' in parsedResponse) {
            errorMessage.value = parsedResponse.message || "No results found for your search.";
        }
        else {
            errorMessage.value = "Unexpected server response.";
        }
    } catch (err) {
        errorMessage.value = `Failed to load results: ${err instanceof Error ? err.message : String(err)}`;
    } finally {
        isLoading.value = false;
    }

};

onMounted(() => {
    fetchResults();
});

watch(
    () => store.searchQuery,
    (newQuery, oldQuery) => {
        if (newQuery !== oldQuery) {
            fetchResults();
        }
    }
);
</script>
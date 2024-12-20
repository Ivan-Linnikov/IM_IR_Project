export const useSearchStore = defineStore('searchStore', () => {
    const searchQuery = ref<string>('');
    const results = ref<any[]>([]);
    const isLoading = ref(false);
    const queryErrorMessage = ref<string | null>(null);
    const filterErrorMessage = ref<string | null>(null);

    const setSearchData = (query: string) => {
        searchQuery.value = query;
    };

    const setResults = (data: any[]) => {
        results.value = data;
    };

    const fetchResults = async () => {
        isLoading.value = true;
        queryErrorMessage.value = null; 
        try {
            const response: any = await $fetch('http://localhost:8000', {
                method: 'POST',
                body: { query: searchQuery.value }, 
            });

            let parsedResponse = typeof response === 'string' ? JSON.parse(response) : response;

            if (Array.isArray(parsedResponse) && parsedResponse.length > 0) {
                setResults(parsedResponse); 
            } else {
                queryErrorMessage.value = "No results found for your search.";
            }
        } finally {
            isLoading.value = false;
        }
    };

    return { 
        searchQuery,  
        results, 
        isLoading, 
        queryErrorMessage, 
        filterErrorMessage,
        setSearchData, 
        setResults, 
        fetchResults 
    };
}, 
);

export const useSearchStore = defineStore('searchStore', () => {
    const searchQuery = ref<string>(''); // This will now stay reactive across all pages
    const results = ref<any[]>([]);
    const isLoading = ref(false);
    const errorMessage = ref<string | null>(null);

    const setSearchData = (query: string) => {
        searchQuery.value = query;
    };

    const setResults = (data: any[]) => {
        results.value = data;
    };

    const fetchResults = async () => {
        isLoading.value = true;
        errorMessage.value = null; // Clear error before new fetch
        try {
            const response: any = await $fetch('http://localhost:8000', {
                method: 'POST',
                body: { query: searchQuery.value }, // Ensure you send the correct query
            });
            console.log('Raw Response from API:', response);
    
            let parsedResponse;
            try {
                parsedResponse = typeof response === 'string' ? JSON.parse(response) : response;
            } catch (err) {
                console.error('Response parsing error', err);
                errorMessage.value = 'Server returned an invalid response.';
                return;
            }
    
            if (Array.isArray(parsedResponse) && parsedResponse.length > 0) {
                setResults(parsedResponse); 
            } else if (Array.isArray(parsedResponse) && parsedResponse.length === 0) {
                errorMessage.value = "No results found for your search.";
            } else if (typeof parsedResponse === 'object' && parsedResponse !== null && 'message' in parsedResponse) {
                errorMessage.value = parsedResponse.message || "No results found for your search.";
            }
            
        } catch (err) {
            errorMessage.value = `Failed to load results: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            isLoading.value = false;
        }
    };

    return { 
        searchQuery,  
        results, 
        isLoading, 
        errorMessage, 
        setSearchData, 
        setResults, 
        fetchResults 
    };
});

export const useSearchStore = defineStore('searchStore', () => {
    const searchQuery = ref<string>('');
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
        errorMessage.value = null; 
        try {
            const response: any = await $fetch('http://localhost:8000', {
                method: 'POST',
                body: { query: searchQuery.value }, 
            });
    
            let parsedResponse = typeof response === 'string' ? JSON.parse(response) : response;
    
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
}, 
{
    persist: true // Correct position for persist option
});

// ~/stores/searchStore.ts
import { defineStore } from 'pinia';

export const useSearchStore = defineStore('search', {
  state: () => ({
    searchQuery: '',
    location: '',
    date: '',
    time: '',
    results: [] as any[] // Holds the entire array of results from the backend
  }),
  actions: {
    setSearchData(query: string, location: string, date: string, time: string) {
      this.searchQuery = query;
      this.location = location;
      this.date = date;
      this.time = time;
    },
    setResults(results: any[]) {
      this.results = results; // Directly store the array
    }
  }
});

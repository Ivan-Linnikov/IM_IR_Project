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
                            class="outline-none focus:outline-none focus:ring-0 focus:bg-transparent bg-white text-[#111111] placeholder-[#111111] flex-1 min-w-0" />

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
                            class="outline-none focus:outline-none focus:ring-0 bg-white text-[#111111] flex-1 min-w-0 cursor-pointer" />
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
        <div v-if="!store.isLoading && !store.queryErrorMessage" class="grid grid-cols-2 gap-10 mt-20 items-start">
            <Card v-for="item in store.results" :key="item.docno" :item="item" @mark-relevant="markAsRelevant"
                @mark-not-relevant="markAsNotRelevant" />
        </div>
        <div v-if="!store.isLoading && store.filterErrorMessage"
            class="mt-20 text-center text-[#111111]">
            <h2 class="text-2xl font-bold">No results found</h2>
            <p>Try adjusting your filters. </p>
            <p class="text-gray-500">The search should be within Switzerland.</p>
        </div>
        <div v-if="!store.isLoading && store.queryErrorMessage" class="mt-20 text-center text-[#111111]">
            <h2 class="text-2xl font-bold">{{ store.queryErrorMessage }}</h2>
            <p>Try adjusting your search criteria or using different keywords.</p>
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
    'Aadorf', 'Aarau', 'Aarau Rohr', 'Aarburg', 'Aarwangen', 'Abtwil SG', 'Adelboden', 'Adlikon b', 'Adliswil', 
    'Aegerten', 'Aesch', 'Aesch LU', 'Affoltern am Albis', 'Agno', 'Aigle', 'Algetshausen', 'Alle', 'Allschwil', 
    'Alpnach Dorf', 'Altbüron', 'Altdorf', 'Altdorf UR', 'Altendorf', 'Altstätten SG', 'Amlikon-Bissegg', 'Amriswil', 
    'Andeer', 'Anglikon', 'Appenzell', 'Apples', 'Aproz', 'Arbon', 'Arch', 'Arlesheim', 'Arni AG', 'Ascona', 
    'Attalens', 'Attiswil', 'Au SG', 'Aubonne', 'Auenstein', 'Aumont', 'Auw', 'Avegno', 'Aven', 'Avenches', 
    'Avry-sur-Matran', 'Avully', 'Azmoos', 'B', 'Baar', 'Bachenbülach', 'Bad Ragaz', 'Bad Zurzach', 'Baden', 
    'Balerna', 'Balsthal', 'Balzers', 'Bannwil', 'Basel', 'Bassecourt', 'Bassersdorf', 'Bauma', 'Belfaux', 'Bellach', 
    'Bellinzona', 'Belp', 'Belprahon', 'Benken SG', 'Bercher', 'Berg', 'Berikon', 'Beringen', 'Berlens', 'Bern', 
    'Berneck', 'Beromünster', 'Bevaix', 'Bex', 'Bi', 'Biasca', 'Biberist', 'Biel', 'Biel Bienne', 'Biel- Bienne', 
    'Biel-Bienne', 'Bilten', 'Binningen', 'Bioggio', 'Birmensdorf', 'Birmensdorf ZH', 'Birr', 'Birsfelden', 
    'Bischofszell', 'Blignoud', 'Blonay', 'Blumenstein', 'Boll', 'Bolligen', 'Boncourt', 'Bonfol', 'Bonvillars', 
    'Bossonnens', 'Boswil', 'Bottighofen', 'Bottmingen', 'Boudry', 'Bouveret', 'Braunau', 'Breganzona', 
    'Breitenbach', 'Bremgarten AG', 'Brig', 'Brissago', 'Bronschhofen', 'Brugg AG', 'Brunnen', 'Brügg BE', 
    'Brügglen', 'Brüttisellen', 'Bubendorf', 'Bubikon', 'Buchrain', 'Buchs AG', 'Buchs SG', 'Buchs ZH', 'Bulle', 
    'Buochs', 'Bure', 'Burgdorf', 'Burgistein', 'Bussigny', 'Buttes', 'Buttikon SZ', 'Buttisholz', 'Buttwil', 
    'Buus', 'Bäretswil', 'Bäriswil BE', 'Bättwil', 'Bühler', 'Bülach', 'Bürchen', 'Büren an der Aare', 'Büron', 
    'Bütschwil', 'Büttikon AG', 'Bützberg', 'Cadenazzo', 'Camorino', 'Campascio', 'Carouge GE', 'Castione', 
    'Celerina', 'Cernier', 'Ch', 'Chailly-Montreux', 'Chalais', 'Cham', 'Champ', 'Chavornay', 'Cheseaux-sur-Lausanne', 
    'Chesi', 'Chevenez', 'Chexbres', 'Chez-le-Bart', 'Chiasso', 'Chippis', 'Chur', 'Clarens', 'Claro', 'Cointrin', 
    'Coldrerio', 'Collombey', 'Colombier', 'Conthey', 'Coppet', 'Corcelles-pr', 'Corin-de-la-Cr', 'Corminboeuf', 
    'Cornaux', 'Corserey', 'Cossonay-Ville', 'Cottens', 'Courgenay', 'Courroux', 'Court', 'Crans-Montana', 'Crissier', 
    'Cugnasco', 'Cugy', 'Cugy VD', 'Dagmersellen', 'Dallenwil', 'Damphreux', 'Davos Dorf', 'Davos Platz', 
    'Deitingen', 'Del', 'Derendingen', 'Develier', 'Dielsdorf', 'Diepoldsau', 'Dietikon', 'Dietlikon', 'Disentis', 
    'Domat', 'Domdidier', 'Dongio', 'Donneloye', 'Dornach', 'Dottikon', 'Duillier', 'Dussnang', 'Däniken', 
    'Dättwil AG', 'Döttingen', 'Dübendorf', 'Düdingen', 'Dürrenroth', 'Ebikon', 'Ebnat-Kappel', 'Echallens', 
    'Echichens', 'Ecublens VD', 'Ecuvillens', 'Effretikon', 'Egerkingen', 'Egg b', 'Eglisau', 'Egliswil', 'Egnach', 
    'Ehrendingen', 'Einsiedeln', 'Elgg', 'Embrach', 'Emmen', 'Emmenbrücke', 'Engelburg', 'Englisberg', 'Ennenda', 
    'Ennetaach', 'Ennetbaden', 'Ennetbürgen', 'Entlebuch', 'Epalinges', 'Erde', 'Erlach', 'Erlen', 'Erlenbach ZH', 
    'Erlenbach im Simmental', 'Erlinsbach', 'Erlinsbach SO', 'Ermatingen', 'Ermensee', 'Ersigen', 'Eschen', 
    'Eschenbach LU', 'Eschenbach SG', 'Eschlikon', 'Escholzmatt', 'Estavayer-le-Lac', 'Ettenhausen', 'Ettingen', 
    'F', 'Farvagny-le-Grand', 'Fehraltorf', 'Fehren', 'Felben-Wellhausen', 'Felsberg', 'Feuerthalen', 'Fiesch', 
    'Fislisbach', 'Flawil', 'Fleurier', 'Flims Dorf', 'Flims Waldhaus', 'Flums', 'Flühli LU', 'Fontainemelon', 
    'Forel', 'Fraubrunnen', 'Frauenfeld', 'Freienbach', 'Freienstein', 'Frenkendorf', 'Fribourg', 'Frick', 'Frutigen', 
    'Fully', 'Fällanden', 'Füllinsdorf', 'Gais', 'Gampelen', 'Gams', 'Gattikon', 'Gebenstorf', 'Gelterkinden', 
    'Geneva', 'Genolier', 'Gerlafingen', 'Gerlikon', 'Gerolfingen', 'Giffers', 'Giornico', 'Gipf-Oberfrick', 'Giswil', 
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
        store.filterErrorMessage = '';

        const response = await $fetch('http://localhost:8000/result', {
            method: 'POST',
            body: filters,
        });

        store.results = response as any[];
        console.log('Results:', store.results);

        // Check if the results are empty
        if (store.results.length === 0) {
            store.filterErrorMessage = 'No results found.';
        }

    } catch (error) {
        store.filterErrorMessage = 'An error occurred while applying filters.';
    } finally {
        store.isLoading = false;

        cityInput.value = ''; 
        (document.getElementById('day') as HTMLSelectElement).value = ''; 
        if (timeInput.value) {
            timeInput.value.value = ''; 
        }
    }
}


function markAsRelevant(docno: string): void {
    const index = store.results.findIndex(item => item.docno === docno);
    if (index !== -1) {
        const [item] = store.results.splice(index, 1); // Remove the item
        store.results.unshift(item); // Add it to the beginning
    }
}

function markAsNotRelevant(docno: string): void {
    store.results = store.results.filter(item => item.docno !== docno); // Remove the item
}
</script>

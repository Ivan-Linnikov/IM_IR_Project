<template>
    <div class="bg-white border border-gray-300 rounded-xl p-6 min-h-40 shadow-xl hover:shadow-2xl transition-shadow font-quicksand">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-2xl font-black font-raleway text-[#111111]">{{ item.Name }}</h3>
        <div class="ml-auto flex items-center space-x-2 relative">
          <div class="relative group">
            <Icon
              icon="mdi:plus"
              class="bg-black text-white w-6 h-6 p-1 rounded-full transition-all duration-300 hover:border hover:border-black hover:bg-white hover:text-[#111111] cursor-pointer"
            />
            <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-black text-white text-xs rounded-lg px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              Relevant
            </div>
          </div>
          <div class="relative group">
            <Icon
              icon="mdi:minus"
              class="bg-black text-white w-6 h-6 p-1 rounded-full transition-all duration-300 hover:border hover:border-black hover:bg-white hover:text-[#111111] cursor-pointer"
            />
            <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-black text-white text-xs rounded-lg px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              Not Relevant
            </div>
          </div>
        </div>
      </div>
  
      <div class="flex">
        <div class="w-1/2 pr-4">
          <div v-if="item.Categories && item.Categories.length > 0" class="text-[#111111] text-l font-semibold mb-4">
            <p>{{ item.Categories.join(', ') }}</p>
          </div>
          <div v-if="item.Address" class="flex items-center text-[#111111] text-l font-semibold mb-4">
            <Icon icon="mdi-light:map-marker" class="w-5 h-5 mr-2 inline-block" />
            <span>{{ item.Address }}</span>
          </div>
        </div>
  
        <div class="w-px bg-gray-300 mx-4"></div>
  
        <div class="w-1/2 pl-4">
          <div v-if="item.Mobile" class="flex items-center text-[#111111] text-l font-semibold mb-4">
            <Icon icon="mdi-light:phone" class="w-5 h-5 mr-2 inline-block" />
            <span>{{ item.Mobile }}</span>
          </div>
          <div v-if="item.Email" class="flex items-center text-[#111111] text-l font-semibold mb-4">
            <Icon icon="line-md:email" class="w-5 h-5 mr-2 inline-block" />
            <span>{{ item.Email }}</span>
          </div>
        </div>
      </div>
  
      <button
        v-if="item.OpeningTimes"
        @click="toggleOpeningHours(getDocno(item))"
        class="flex items-center justify-between w-full mt-6 text-[#111111] text-l font-black cursor-pointer"
      >
        <span class="flex items-center">
          <Icon icon="mdi-light:clock" class="w-5 h-5 mr-2" /> Opening Times
        </span>
        <Icon
          icon="oui:arrow-down"
          :class="{ 'rotate-180': isOpen(getDocno(item)) }"
          class="w-6 h-6 transform transition-transform"
        ></Icon>
      </button>
  
      <div
        v-if="item.OpeningTimes"
        :class="isOpen(getDocno(item)) ? 'opacity-100' : 'max-h-0 opacity-0'"
        class="transition-all duration-300 overflow-hidden mt-4"
      >
        <ul class="p-2 space-y-4 text-[#111111] text-l font-semibold">
          <li v-for="([day, time], index) in Object.entries(item.OpeningTimes)" :key="index" class="flex justify-between">
            <span>{{ cleanDay(day) }}:</span>
            <span>{{ time }}</span>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { Icon } from '@iconify/vue/dist/iconify.js';
  import { defineProps, ref } from 'vue';
  
  interface SearchResult {
    id: number;
    Name: string;
    Address?: string;
    Mobile?: string | null;
    Email?: string | null;
    Categories?: string[];
    OpeningTimes?: Record<string, string>;
    docno?: string;
  }
  
  defineProps({
    item: {
      type: Object as () => SearchResult,
      required: true,
    },
  });
  
  const openCards = ref<number[]>([]);
  
  function getDocno(item: SearchResult): number {
    const docno = Number(item.docno);
    if (!isNaN(docno)) return docno;
    if (item.id) return item.id;
    return Math.random();
  }
  
  function toggleOpeningHours(id: number) {
    if (openCards.value.includes(id)) {
      openCards.value = openCards.value.filter((openId) => openId !== id);
    } else {
      openCards.value.push(id);
    }
  }
  
  function isOpen(id: number): boolean {
    return openCards.value.includes(id);
  }
  
  function cleanDay(day: string): string {
    return day.replace(/\W+/g, '').trim(); // Remove non-word characters and trim spaces
  }
  </script>

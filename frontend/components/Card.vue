<template>
    <div class="bg-white border border-gray-300 rounded-xl p-6 min-h-96 shadow-xl hover:shadow-2xl transition-shadow font-quicksand">

      <h3 class="text-2xl font-black font-raleway text-[#111111] mb-4">{{ item.title }}</h3>

      <div v-if="item.categories && item.categories.length > 0" class="text-[#111111] text-l font-semibold mb-4">
        <p>{{ item.categories.join(', ') }}</p>
      </div>
  
      <div v-if="item.address" class="flex items-center text-[#111111] text-l font-semibold mb-4">
        <Icon icon="mdi-light:map-marker" class="w-5 h-5 mr-2 inline-block" />
        <span>{{ item.address }}</span>
      </div>
  
      <hr class="border-t border-gray-200 my-4" />
  
      <div v-if="item.mobile" class="flex items-center text-[#111111] text-l font-semibold mb-4">
        <Icon icon="mdi-light:phone" class="w-5 h-5 mr-2 inline-block" />
        <span>{{ item.mobile }}</span>
      </div>
  
      <div v-if="item.email" class="flex items-center text-[#111111] text-l font-semibold mb-4">
        <Icon icon="line-md:email" class="w-5 h-5 mr-2 inline-block" />
        <span>{{ item.email }}</span>
      </div>
  
      <button v-if="item.openingTimes" @click="toggleOpeningHours(item.id)"
        class="flex items-center justify-between w-full mt-6 text-[#111111] text-l font-black cursor-pointer">
        <span class="flex items-center">
          <Icon icon="mdi-light:clock" class="w-5 h-5 mr-2" /> Opening Times
        </span>
        <Icon icon="oui:arrow-down" :class="{ 'rotate-180': isOpen(item.id) }"
          class="w-6 h-6 transform transition-transform"></Icon>
      </button>
  
      <div v-if="item.openingTimes"
        :class="isOpen(item.id) ? 'opacity-100' : 'max-h-0 opacity-0'"
        class="transition-all duration-300 overflow-hidden mt-4">
        <ul class="p-2 space-y-4 text-[#111111] text-l font-semibold">
          <li v-for="(time, day) in item.openingTimes" :key="day" class="flex justify-between">
            <span>{{ day }}:</span>
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
    title: string;
    address?: string;
    mobile?: string | null;
    email?: string | null;
    categories?: string[];
    openingTimes?: Record<string, string>;
  }
  
  defineProps({
    item: {
      type: Object as () => SearchResult,
      required: true,
    },
  });
  
  const openCards = ref<number[]>([]);
  
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
  </script>
  
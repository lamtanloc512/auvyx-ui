<script setup lang="ts">
import type {} from './auvyx-types/vue';
import { ref } from 'vue';
const tab = ref<string>('account');
const open = ref(false);
function onTab(e: CustomEvent<{ value: string | null }>) { tab.value = e.detail.value ?? ''; }
</script>
<template>
  <auvyx-tabs :value="tab" @change="onTab"><div class="tabs" /></auvyx-tabs>
  <auvyx-drawer :open="open" @toggle="(e) => (open = e.detail.open)" />
  <auvyx-command @select="(e) => console.log(e.detail.value)" />
  <!-- @vue-expect-error open is boolean -->
  <auvyx-popover :open="'yes'" />
</template>

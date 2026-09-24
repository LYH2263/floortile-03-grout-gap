<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>缝宽 {{ result.gap_mm ?? 0 }} mm，有效单片 {{ result.piece_m2 }} m²</li>
      <li>地面 {{ result.area_m2 }} m²</li>
    </ul>
  </div>
</template>

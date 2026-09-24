<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const settings = ref({})
const gapMm = ref(0)
const msg = ref('')
const err = ref('')

onMounted(async () => {
  settings.value = await getJSON('/api/settings')
  gapMm.value = Number(settings.value.gap_mm) || 0
})

async function save() {
  msg.value = ''
  err.value = ''
  try {
    settings.value = await putJSON('/api/settings', { gap_mm: gapMm.value })
    gapMm.value = Number(settings.value.gap_mm) || 0
    msg.value = '已保存默认缝宽'
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按面积法向上取整后再乘 (1+损耗%)。</p>
    <p>当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>
    <p>有效边长 = 砖边长 − 缝宽，有效单片面积进入面积法净用量，再加损耗得订货片数。</p>
    <label>默认缝宽(mm) <input type="number" min="0" step="0.5" v-model.number="gapMm"></label>
    <button @click="save">保存默认缝宽</button>
    <p v-if="msg">{{ msg }}</p>
    <p v-if="err" class="alert">{{ err }}</p>
    <p>默认缝宽仅用于新单；历史记录按保存时的缝宽与片数回放。</p>
    <p>网格预览块数可能大于面积法片数，下单以面积法 order_count 为准。</p>
  </div>
</template>

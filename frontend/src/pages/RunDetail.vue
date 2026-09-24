<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'
import TileGridPreview from '../components/TileGridPreview.vue'
const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')
onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = '记录不存在或已删除'
  }
})
</script>
<template>
  <div class="page">
    <h1>测算记录 #{{ id }}</h1>
    <p v-if="err" class="alert">{{ err }}</p>
    <template v-if="run">
      <p class="alert">历史快照，未重新计算</p>
      <dl>
        <dt>时间</dt><dd>{{ run.created_at?.slice(0, 19) }}</dd>
        <dt>房间</dt><dd>{{ run.room_name }}</dd>
        <dt>砖型</dt><dd>{{ run.tile_name }}</dd>
        <dt>备注</dt><dd>{{ run.note }}</dd>
      </dl>
      <OrderSummary :result="run.result" />
      <TileGridPreview v-if="run.result?.layout" :cols="run.result.layout.cols" :rows="run.result.layout.rows" :grid-count="run.result.layout.grid_count" />
    </template>
    <router-link to="/history">返回记录</router-link>
  </div>
</template>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
    <el-form-item label="部门名称：" prop="name">
      <el-input
          v-model="form.name"
          placeholder="请输入部门名称"
          clearable
          class="!w-[180px]"
        />
    </el-form-item>
    <el-form-item>
        <el-button
          type="primary"
          :icon="useRenderIcon('ri:search-line')"
          :loading="loading"
          @click=""
        >
          搜索
        </el-button>
        <el-button :icon="useRenderIcon(Refresh)" @click="">
          重置
        </el-button>
      </el-form-item>
    </el-form>

    
  </div>
</template>

<script setup>
defineOptions({
  name: "Department"
})

import { useRenderIcon } from "@/components/ReIcon/src/hooks"
import { ref, reactive } from 'vue'

import Refresh from "@iconify-icons/ep/refresh"

const formRef = ref()
const form = reactive({})
const loading = ref(false)
const columns = reactive({})
</script>

<style lang='scss' scoped>
:deep(.el-table__inner-wrapper::before) {
  height: 0;
}

.main-content {
  margin: 24px 24px 0 !important;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>

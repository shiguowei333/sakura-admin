<template>
  <div class="maincontent">
    <!-- 筛选搜索区域 -->
    <div class="top">
      <el-form ref="formRef" :inline="true" :model="form" class="searchform">
        <el-form-item label="部门名称：" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" clearable class="!w-[180px]" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="useRenderIcon('ri:search-line')" :loading="loading" @click=""> 搜索 </el-button>
          <el-button :icon="useRenderIcon('ri:refresh-line')" @click=""> 重置 </el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格数据区域 -->
    <div ref="tableContainer" class="table">
      <div class="title">
        <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">部门管理</span>
        <el-button type="primary" :icon="useRenderIcon('ri:add-circle-line')"> 新增 </el-button>
      </div>
      <el-table :data="dataList" style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all :header-cell-style="{'background-color': 'var(--el-fill-color-light)','color': 'var(--el-text-color-primary)'}">
        <el-table-column prop="name" label="部门名称" />
        <el-table-column prop="leader" label="部门领导" />
        <el-table-column prop="rank" label="排序" sortable />
        <el-table-column prop="remark" label="备注" />
        <el-table-column label="操作" align="center" fixed="right" min-width="100px">
          <template #default="{ row }">
            <div class="ellink">
              <el-link :underline="false" type="primary" @click="handleEdit(row)">新增</el-link>
              <el-link :underline="false" type="primary" @click="handleCreat(row.id)">编辑</el-link>
              <el-link :underline="false" type="danger" @click="handleDelete(row)">删除</el-link>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from "vue";
import { handleTree } from "@/utils/tree";
import deptdialog from "./components/deptdialog.vue";
import { getDepartmentList, addDepartment, updateDepartment, deleteDepartment } from "@/api/system/department";
import { isAllEmpty } from "@pureadmin/utils";
import { ElMessage, ElMessageBox } from "element-plus";
import { message } from "@/utils/message";

const formRef = ref(null);

defineOptions({
  name: "department"
});

// 筛选过滤器数据
const form = reactive({
  name: ""
});
const loading = ref(false);
const dataList = ref([]);

const getDeptData = async () => {
  let res = await getDepartmentList(form)
  dataList.value =  handleTree(res.data, 'id', 'parent')
  console.log(dataList.value)
}



// 弹窗相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedDept = ref({});


onMounted(() => {
  getDeptData()
});

</script>

<style lang="scss" scoped>
::v-deep(.el-table .cell) {
  overflow: hidden; // 溢出隐藏
  text-overflow: ellipsis; // 溢出用省略号显示
  white-space: nowrap; // 规定段落中的文本不进行换行
}

.main-content {
  margin: 24px 24px 0 !important;
}

.maincontent {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 141px);
}

.searchform {
  background-color: var(--el-bg-color);
  /* padding: 10px; */
  .el-form-item {
    margin: 10px;
  }
}

.title {
  margin: 10px;
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

.table {
  overflow: hidden;
  flex: 1;
  margin-top: 10px;
  background-color: var(--el-bg-color);
  /* 解决element表格在flex布局下无法自适应窗口宽度缩小的问题 */
  position: relative;
  .el-table {
    position: absolute;
  }
}

.ellink {
  display: flex;
  gap: 10px;
  justify-content: center;
}
</style>
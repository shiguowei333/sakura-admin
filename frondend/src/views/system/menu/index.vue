<template>
    <div class="maincontent">
      <!-- 筛选搜索区域 -->
      <div class="top">
        <el-form ref="formRef" :inline="true" :model="form" class="searchform">
          <el-form-item label="菜单名称：" prop="name">
            <el-input v-model="form.name" placeholder="请输入菜单名称" clearable class="!w-[180px]" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="useRenderIcon(Search)" :loading="loading" @click="onSearch"> 搜索 </el-button>
            <el-button :icon="useRenderIcon(Reset)" @click="onReset"> 重置 </el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- 表格数据区域 -->
      <div ref="tableContainer" class="table">
        <div class="title">
          <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">菜单管理</span>
          <el-button type="primary" :icon="useRenderIcon(Add)" @click="handleOnAdd"> 新增 </el-button>
        </div>
        <div class="inner-table">
          <el-table :data="dataList" class="el-table" height="100%" style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all :header-cell-style="{'background-color': 'var(--el-fill-color-light)','color': 'var(--el-text-color-primary)'}">
          <el-table-column label="菜单名称" style="">
            <template #default="{ row }">
                <IconifyIconOnline style="display: inline-block; vertical-align: middle;" :icon="row.meta.icon" />&nbsp;{{ row.meta.title }}
            </template>
          </el-table-column>
          <el-table-column prop="menu_type" label="菜单类型" >
            <template #default="{ row }">
                <el-tag :type="menuType(row.menu_type)[0]" effect="plain">{{ menuType(row.menu_type)[1] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="route_name" label="路由名称" />
          <el-table-column prop="route_path" label="路由路径" />
          <el-table-column prop="meta.rank" label="排序" />
          <el-table-column label="操作" align="center" fixed="right" min-width="100px">
            <template #default="{ row }">
              <div class="ellink">
                <el-link :underline="false" type="primary" @click="handleOnAdd(e, row.id)">新增</el-link>
                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
              </div>
            </template>
          </el-table-column>
        </el-table>
        </div>
      </div>
      <!-- 新增/编辑表单 -->
      <el-dialog v-model="isDialogVisible" :title="isEditMode ? '编辑部门' : '新增部门'" :width="'40%'">
          <el-form ref="deptFormRef" :model="deptData" :rules="rules" label-width="80px" label-position="right">
            <el-form-item label="部门名称" prop="name">
              <el-input v-model="deptData.name" maxlength="20" show-word-limit placeholder="请输入部门名称" />
            </el-form-item>
            <el-form-item label="部门领导" prop="leader">
              <el-input v-model="deptData.leader" maxlength="20" show-word-limit placeholder="请输入部门领导名称" />
            </el-form-item>
            <el-form-item label="部门排序" prop="rank">
              <el-input-number v-model="deptData.rank":min="1" :max="999" :value-on-clear="1" controls-position="right" />
            </el-form-item>
            <el-form-item label="上级部门" prop="parent">
              <el-cascader v-model="deptData.parent" :options="dataList" :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }" clearable filterable :show-all-levels="false" placeholder="无上级部门" />
            </el-form-item>
            <el-form-item label="备注" prop="remark">
              <el-input v-model="deptData.remark" maxlength="50" type="textarea" show-word-limit placeholder="请输入备注" />
            </el-form-item>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="isDialogVisible=false">取消</el-button>
              <el-button type="primary" @click="handleAdd">确认</el-button>
            </div>
          </template>
        </el-dialog>
        <!-- 删除确认弹窗 -->
        <el-dialog v-model="isDelDialogVisible" title="提示" width="500" align-center>
          <p>是否确认删除"{{ deptData.name }}"</p>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="isDelDialogVisible=false">取消</el-button>
              <el-button type="primary" @click="handleDel">确认</el-button>
            </div>
          </template>
        </el-dialog>
      </div>
  </template>
  
  <script setup>
  import { useRenderIcon } from "@/components/ReIcon/src/hooks";
  import { ref, reactive, onMounted, nextTick } from "vue";
  import { handleTree, getParentPath } from "@/utils/tree";
  import { getMenuList, addMenu, updateMenu, deleteMenu } from "@/api/system/menu";
  import { ElMessage, ElMessageBox } from "element-plus";
  import Search from "@iconify-icons/ri/search-line";
  import Reset from "@iconify-icons/ri/refresh-line";
  import Add from "@iconify-icons/ri/add-circle-line"
  
  
  defineOptions({
    name: "department"
  });
  
  // 搜索区域相关
  const formRef = ref(null);
  const form = reactive({
    name: ""
  });
  const loading = ref(false);
  
  // 搜索点击事件
  const onSearch = async() => {
    loading.value = true
    let res = await getMenuData()
    if(res.code = 2000) {
      loading.value = false
    }
  }
  
  // 重置点击事件
  const onReset = () => {
    form.name = ''
    getMenuData()
  }
  
  //数据展示区域
  const dataList = ref([]);
  
  const getMenuData = async () => {
    let res = await getMenuList(form.name)
    if(res.code == 2000) {
      dataList.value =  handleTree(res.data, 'id', 'parent')
      return res
    }
  }
  // 
  const menuType = (menu_type) => {
    switch(menu_type) {
        case 0:
            return ['primary', '菜单']
        case 1:
            return ['success', 'iframe']
        case 2:
            return ['warning', '外链']
        case 3:
            return ['danger', '按钮']
        default:
            return ['', '']
    }
  }
  
  
  
//   // 表单相关
//   const isDialogVisible = ref(false);
//   const isEditMode = ref(false);
//   const deptFormRef = ref(null)
//   const deptData = ref({
//     id: '',
//     name: '',
//     leader: '',
//     rank: 99,
//     parent: null,
//     remark: ''
//   })
//   // 校验规则
//   const rules = reactive({
//     name: [{required: true, message: '请输入部门名称', trigger: 'blur'}],
//     leader: [{required: true, message: '请输入部门领导名称', trigger: 'blur'}],
//     rank: [{required: true, message: '请输入部门排序', trigger: 'blur'}]
//   })
//   // 处理新增按钮点击事件逻辑
//   const handleOnAdd = async(e,id) => {
//     isEditMode.value = false
//     isDialogVisible.value = true
//     await nextTick()
//     deptFormRef.value.resetFields()
//     // 需要获取该节点和祖先节点全路径
//     deptData.value.parent = getParentPath(dataList.value, id)
  
//   }
//   // 处理编辑按钮点击事件逻辑
//   const handleOnEdit = async(e, row) => {
//     isEditMode.value = true
//     isDialogVisible.value = true
//     await nextTick()
//     deptFormRef.value.resetFields()
//     deptData.value.id = row.id
//     deptData.value.name = row.name
//     deptData.value.leader = row.leader
//     deptData.value.rank = row.rank
//     deptData.value.remark = row.remark
  
//     // 需要获取祖先节点全路径
//     deptData.value.parent = getParentPath(dataList.value, row.parent)
//   }
  
//   // 处理提交事件
//   const handleAdd = () => {
//     deptFormRef.value.validate(async(valid) => {
//       if(valid){
//         let data = deptData.value
//         if(deptData.value.parent) {
//           data.parent = data.parent[data.parent.length-1]
//         }
//         let res = isEditMode.value?await updateDepartment(deptData.value.id, deptData.value):await addDepartment(deptData.value)
//         if(res.code == 2000) {
//           isDialogVisible.value = false
//           getDeptData()
//           ElMessage({
//            type: 'success',
//            message: isEditMode.value?'编辑成功':'新增成功'
//          })
//         }else {
//           return false
//         }
//       }
//     })
//   }
  
//   // 删除部门相关
//   const isDelDialogVisible = ref(false)
  
//   // 处理删除按钮点击事件逻辑
//   const handleOnDel = (e, row) => {
//     isDelDialogVisible.value = true
//     deptData.value = Object.assign(row)
//   }
  
//   const handleDel = async() => {
    
//     try {
//       let res = await deleteDepartment(deptData.value.id)
//       if(res.code == 2000) {
//         getDeptData()
//         ElMessage({
//            type: 'success',
//            message: '删除成功'
//         })
//       }
//     } catch (error) {
//       ElMessage({
//         type: 'error',
//         message: '删除失败，该部门下存在子部门！'
//       })
//     } finally {
//       isDelDialogVisible.value = false
//     }
//   }
  
  onMounted(() => {
    getMenuData()
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
        margin: 15px 20px;
    }
  }
  
  .title {
    margin: 10px;
    padding: 10px;
    display: flex;
    justify-content: space-between;
  }
  
  .table {
    display: flex;
    flex-direction: column;
    flex: 1;
    margin-top: 10px;
    background-color: var(--el-bg-color);
    /* 解决element表格在flex布局下无法自适应窗口宽度缩小的问题 */
    .inner-table {
      flex: 1;
      position: relative;
      .el-table {
      position: absolute;
      }
    }
  }
  
  .ellink {
    display: flex;
    gap: 10px;
    justify-content: center;
  }
  
  .dialog-footer {
    text-align: right;
  }
  </style>
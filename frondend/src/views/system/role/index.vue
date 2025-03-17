<template>
    <div class="maincontent">
        <!-- 筛选搜索区域 -->
        <div class="top">
            <el-form ref="formRef" :inline="true" :model="form" class="searchform">
                <el-form-item label="角色名称：" prop="name">
                    <el-input v-model="form.name" placeholder="请输入角色名称" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item label="角色标识：" prop="code">
                    <el-input v-model="form.code" placeholder="请输入角色标识" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :icon="useRenderIcon(Search)" :loading="loading" @click="onSearch"> 搜索
                    </el-button>
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
                <el-table :data="dataList" class="el-table" height="100%"
                    style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all
                    :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'color': 'var(--el-text-color-primary)' }">
                    <el-table-column prop="name" label="角色名称" />
                    <el-table-column prop="code" label="角色标识" />
                    <el-table-column prop="mark" label="备注" />
                    <el-table-column prop="create_time" label="创建时间" />
                    <el-table-column label="操作" align="center" fixed="right" min-width="100px">
                        <template #default="{ row }">
                            <div class="ellink">
                                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                                <el-link :underline="false" type="primary" @click="">权限</el-link>
                                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <!-- 新增/编辑表单 -->

    </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, nextTick } from "vue";
import { getRoleList, addRole, updateRole, deleteRole } from "@/api/system/role";
import { ElMessage, ElMessageBox } from "element-plus";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line"


defineOptions({
    name: "role"
});

// 搜索区域相关
const formRef = ref(null);
const form = reactive({
    name: "",
    code: ""
});
const loading = ref(false);

// 搜索点击事件
const onSearch = async () => {
    loading.value = true
    let res = await getRoleData()
    if (res.code = 2000) {
        loading.value = false
    }
}

// 重置点击事件
const onReset = () => {
    formRef.value.resetFields()
    getRoleData()
}

//数据展示区域
const dataList = ref([]);

const getRoleData = async () => {
    let res = await getRoleList(form)
    if (res.code == 2000) {
        dataList.value = res.data
        return res
    }
}



// 表单相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const roleFormRef = ref(null)
const roleData = ref({
    id: '',
    name: '',
    code: '',
    mark: '',
    create_time: '',
    menus: []
})

// 校验规则
const rules = reactive({
    title: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
})
// 处理新增按钮点击事件逻辑
const handleOnAdd = async (e, id) => {
    isEditMode.value = false
    isDialogVisible.value = true
    await nextTick()
    initForm()
    // 需要获取该节点和祖先节点全路径
    menuData.value.parent = getParentPath(dataList.value, id)
}
// 处理编辑按钮点击事件逻辑
const handleOnEdit = async (e, row) => {
    isEditMode.value = true
    isDialogVisible.value = true
    await nextTick()
    initForm()
    for (const k in row) {
        menuData.value[k] = row[k]
    }
    // 需要获取祖先节点全路径
    menuData.value.parent = getParentPath(dataList.value, row.parent)
}

// 处理提交事件
const handleAdd = () => {
    menuFormRef.value.validate(async (valid) => {
        if (valid) {
            let data = menuData.value
            if (menuData.value.parent) {
                data.parent = data.parent[data.parent.length - 1]
            }
            switch (data.menu_type) {
                case 0:
                    data.code = ''
                    data.frameSrc = ''
                    break;
                case 1:
                    data.code = ''
                    data.component = ''
                    data.redirect = ''
                    break;
                case 2:
                    data.code = ''
                    data.component = ''
                    data.redirect = ''
                    data.enterTransition = ''
                    data.leaveTransition = ''
                    data.frameSrc = ''
                    break;
                case 3:
                    data.route_name = ''
                    data.route_path = ''
                    data.icon = ''
                    data.component = ''
                    data.redirect = ''
                    data.enterTransition = ''
                    data.leaveTransition = ''
                    data.frameSrc = ''
                    break;
                default:
                    break;
            }
            let res = isEditMode.value ? await updateMenu(data.id, data) : await addMenu(data)
            if (res.code == 2000) {
                isDialogVisible.value = false
                getMenuData()
                ElMessage({
                    type: 'success',
                    message: isEditMode.value ? '编辑成功' : '新增成功'
                })
            } else {
                return false
            }
        }
    })
}

const initForm = () => {
    menuData.value.id = '',
        menuData.value.route_name = '',
        menuData.value.route_path = '',
        menuData.value.menu_type = 0,
        menuData.value.component = '',
        menuData.value.code = '',
        menuData.value.title = '',
        menuData.value.icon = '',
        menuData.value.rank = 99,
        menuData.value.showLink = true,
        menuData.value.showParent = false,
        menuData.value.keepAlive = false,
        menuData.value.frameSrc = '',
        menuData.value.frameLoading = true,
        menuData.value.hiddenTag = false,
        menuData.value.fixedTag = false,
        menuData.value.enterTransition = '',
        menuData.value.leaveTransition = '',
        menuData.value.parent = '',
        menuData.value.redirect = ''
}


// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {

    ElMessageBox.confirm(
        `是否确认删除角色'${row.title}'?`,
        '提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            try {
                let res = await deleteMenu(row.id)
                if (res.code == 2000) {
                    getMenuData()
                    ElMessage({
                        type: 'success',
                        message: '删除成功'
                    })
                }
            } catch (error) {
                ElMessage({
                    type: 'error',
                    message: '删除失败，该菜单下存在子菜单！'
                })
            }
        })
}

onMounted(() => {
    getRoleData()
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
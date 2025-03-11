import { http } from '@/utils/http'

const url = '/system/department/'

export const getDepartmentList = (form) => http.get(url)

export const addDepartment = () => http.post(url)

export const updateDepartment = (id, data) => http.put(url + id, data)

export const deleteDepartment = (id) => http.delete(url + id)
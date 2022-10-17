// repository which provides methods for ingredients and ingredient groups
import Repository from './Repository'

const resource = '/ingredients'

export default {
  listTopLevelGroups () {
    return Repository.get(`${resource}/groups`)
  },
  getGroup(groupId) {
    return Repository.get(`${resource}/groups/${groupId}`)
  },
  createGroup(data) {
    return Repository.put(`${resource}/groups`, data)
  },
  createIngredient(data) {
    return Repository.put(`${resource}`, data)
  },
  updateIngredient(ingredientId, data) {
    return Repository.post(`${resource}/${ingredientId}`, data)
  },  
  search (searchTerm) {
    return Repository.get(`${resource}?q=${searchTerm}`)
  },
}

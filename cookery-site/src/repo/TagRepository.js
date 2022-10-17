// repository which provides methods for ingredients and ingredient groups
import Repository from './Repository'

const resource = '/tags'

export default {
  search (searchTerm) {
    return Repository.get(`${resource}?q=${searchTerm}`)
  },
  listCategories (group) {
    return Repository.get(`${resource}/categories?group=${group}`)
  },
}

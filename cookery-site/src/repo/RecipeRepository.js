// repository which provides methods for vehicles
import Repository from './Repository'

const resource = '/recipes'

export default {
  list (group, page, per_page, q, sortOrder, ingredients, tags) {
    return Repository.get(`${resource}?group=${group}&page=${page}&perPage=${per_page}&q=${q}&sortOrder=${sortOrder}&ingredients=${ingredients.join(';')}&tags=${tags.join(';')}`)
  },
  listLatest (groupName, count) {
    return Repository.get(`${resource}/latest?group=${groupName}&count=${count}`)
  },
  get (recipeId) {
    return Repository.get(`${resource}/${recipeId}`)
  },
  create (data) {
    return Repository.put(`${resource}`, data)
  },
  update (recipeId, data) {
    return Repository.post(`${resource}/${recipeId}`, data)
  },
  uploadRecipeImage (recipeId, imageFile) {
    let formData = new FormData();
    formData.append('image', imageFile);
    Repository.post(`${resource}/${recipeId}/image`,
       formData,
       {
         headers: { 'Content-Type': 'multipart/form-data' }
       });
  }
}

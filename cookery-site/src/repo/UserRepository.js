// repository which provides methods for user data and session management
import Repository from './Repository'

const resource = '/user'

export default {
  login (uname, pwd) {
    return Repository.post(`${resource}/login`, {
      username: uname,
      password: pwd
    })
  },
  change_pwd(old_pwd, new_pwd) {
    return Repository.post(`${resource}/my/password`, {
      old_password: old_pwd,
      new_password: new_pwd
    })
  },
  logout () {
    return Repository.get(`${resource}/logout`)
  }
}

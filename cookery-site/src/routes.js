const LoginView = () => import('./components/Login.vue')
const MainView = () => import('./components/Main.vue')
const NotFoundView = () => import('./components/404.vue')

const EmptyRouterView = () => import('./components/views/EmptyRouterView.vue')
const HomeView = () => import('./components/views/Home.vue')
const RecipesView = () => import('./components/views/Recipes.vue')
const RecipeDetailsView = () => import('./components/views/RecipeDetails.vue')
const CreateOrEditRecipeView = () => import('./components/views/CreateOrEditRecipe.vue')

const ConfigurationView = () => import('./components/views/Configuration.vue')
const ConfigurationWelcomeView = () => import('./components/views/config/ConfigWelcome.vue')
const ConfigurationIngredientsView = () => import('./components/views/config/ConfigIngredients.vue')
const ConfigurationUserProfileView = () => import('./components/views/config/ConfigUserProfile.vue')

function generate_group_node (path, groupId) {
  return {
    path: path,          
    component: EmptyRouterView,
    children: [
      {
        path: '',
        name: path,
        component: RecipesView,
        props: { groupName: path, groupId: groupId },
        meta: { description: 'Alle Kochrezepte', requiresAuth: true }
      },
      {              
        path: 'neues-rezept',              
        name: path + '-recipe-new',
        component: CreateOrEditRecipeView,              
        props: { groupName: path, groupId: groupId },
        meta: { description: 'Erlaubt das Erstellen eines neuen Rezepts', requiresAuth: true }
      },
      {              
        path: ':id/:readableId?',              
        name: path + '-recipe-details',
        component: RecipeDetailsView,
        props: { groupName: path, groupId: groupId },
        meta: { description: 'Zeigt ein Rezept', requiresAuth: true }
      },
      {              
        path: ':id/:readableId?/bearbeiten',
        name: path + '-recipe-edit',
        component: CreateOrEditRecipeView,              
        props: route => ({ groupName: path, groupId: groupId, editRecipeId: route.params.id }),
        meta: { description: 'Bearbeitet ein Rezept', requiresAuth: true }
      },            
      {
        // forward a recipe url (which only contains an id (without slash))
        path: ':id',              
        redirect: ':id/'
      }
    ]
  }
}

const routes = [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    { path: '/', redirect: '/home' },
    {
      path: '/',
      component: MainView,
      children: [
        {
          path: 'home',
          name: 'Home',
          alias: '',
          component: HomeView,          
          meta: { description: 'Home', requiresAuth: true }
        },    
        generate_group_node('kochen', 0),
        generate_group_node('backen', 1),
        generate_group_node('cocktails', 2),
        {
          path: 'konfiguration',
          component: ConfigurationView,
          children: [
            {
              path: '',
              name: 'config',
              component: ConfigurationWelcomeView
            },
            {
              path: 'zutaten',
              name: 'config-ingredients',
              component: ConfigurationIngredientsView
            },
            {
              path: 'profil',
              name: 'config-user',
              component: ConfigurationUserProfileView
            }
          ]
        }
      ]
    },
    {
      // page not found handler      
      path: '*',      
      component: MainView,
      children: [
        {
          name: '404',
          path: '',
          component: NotFoundView
        }
      ]
    }
]

export default routes
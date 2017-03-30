import App from './App'
import Detail from './components/Detail'
import DetailContent from './components/DetailContent'
import DetailEditor from './components/DetailEditor'
import List from './components/List'
import AuthorProjects from './components/AuthorProjects'
import UserProfile from './components/UserProfile'
import AccountRegistration from './components/AccountRegistration'


export default [
  {
    path: '/',
    component: App,
    children: [{
        name: 'author',
        path: 'author/:id',
        component: AuthorProjects,
        props: true
      }, {
        path: '',
        alias: ['all', 'favourite', 'liked', 'subscribers', 'my'],
        name: 'list',
        component: List,
        props: (route) => ({ showAuthor: route.path !== '/my' })
      }, {
        name: 'detail',
        path: 'detail/:id',
        component: Detail,
        props: true,
        children: [{
            path: '/',
            component: DetailContent
          }, {
            path: 'edit',
            component: DetailEditor
          }
        ]
      }, {
        name: 'profile',
        path: 'profile',
        component: UserProfile,
      }, {
        name: 'registration',
        path: 'registration',
        component: AccountRegistration
      }
    ]
  }
]

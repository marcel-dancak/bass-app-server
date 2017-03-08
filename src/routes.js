import App from './App'
import Detail from './components/Detail'
import List from './components/List'

export default [
    {
      path: '/',
      component: App,
      children: [{
          name: 'author',
          path: 'author/:id',
          component: List,
        }, {
          path: '',
          alias: ['all/', 'favourite/', 'liked/'],
          name: 'list',
          component: List
        }, {
        name: 'detail',
        path: 'detail/:id',
        component: Detail,
        props: true
      }]
    }
]

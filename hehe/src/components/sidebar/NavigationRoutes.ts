export interface INavigationRoute {
  name: string
  displayName: string
  meta: { icon: string }
  children?: INavigationRoute[]
}

export default {
  root: {
    name: '/',
    displayName: 'navigationRoutes.home',
  },
  routes: [
    {
      name: 'dashboard',
      displayName: 'menu.dashboard',
      meta: {
        icon: 'vuestic-iconset-dashboard',
      },
    },
    {
      name: 'new score',
      displayName: 'スコア登録',
      meta: {
        icon: 'add',
      },
    },
    {
      name: 'edit score',
      displayName: '過去のスコア編集',
      meta: {
        icon: 'edit',
      },
    },
    {
      name: 'users',
      displayName: 'menu.users',
      meta: {
        icon: 'group',
      },
    },
    {
      name: 'hdcp',
      displayName: 'menu.hdcp',
      meta: {
        icon: 'edit',
      },
    },
    {
      name: 'payments',
      displayName: '結果',
      meta: {
        icon: 'newspaper',
      },
      children: [
        {
          name: 'payment-methods',
          displayName: '2024',
        },
        {
          name: 'payment-methods',
          displayName: '2025',
        },
        {
          name: 'payment-methods',
          displayName: '2026',
        },
      ],
    },
    {
      name: 'payments',
      displayName: 'ランキング更新',
      meta: {
        icon: 'publish',
      },
    },

    // {
    //   name: 'projects',
    //   displayName: 'menu.projects',
    //   meta: {
    //     icon: 'folder_shared',
    //   },
    // },
    // {
    //   name: 'auth',
    //   displayName: 'menu.auth',
    //   meta: {
    //     icon: 'login',
    //   },
    //   children: [
    //     {
    //       name: 'login',
    //       displayName: 'menu.login',
    //     },
    //     {
    //       name: 'signup',
    //       displayName: 'menu.signup',
    //     },
    //     {
    //       name: 'recover-password',
    //       displayName: 'menu.recover-password',
    //     },
    //   ],
    // },
    {
      name: 'faq',
      displayName: 'menu.faq',
      meta: {
        icon: 'quiz',
      },
    },
    {
      name: '404',
      displayName: 'menu.404',
      meta: {
        icon: 'vuestic-iconset-files',
      },
    },
    // {
    //   name: 'preferences',
    //   displayName: 'menu.preferences',
    //   meta: {
    //     icon: 'manage_accounts',
    //   },
    // },
    // {
    //   name: 'settings',
    //   displayName: 'menu.settings',
    //   meta: {
    //     icon: 'settings',
    //   },
    // },
  ] as INavigationRoute[],
}

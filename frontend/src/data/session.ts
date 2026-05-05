import { computed, reactive, ref } from 'vue'
import { useCall } from 'frappe-ui'
import router from '@/router'

export const sessionUser = ref<string | null>(getSessionUserFromCookie())

interface Session {
  login: any
  logout: any
  user: typeof sessionUser
  roles: string[]
  isLoggedIn: boolean
  hasRole: (role: string | string[]) => boolean
  isAdmin: boolean
}

export const session: Session = reactive({
  login: useCall({
    url: '/api/v2/method/login',
    immediate: false,
    onSuccess(data: any) {
      sessionUser.value = getSessionUserFromCookie()
      session.login.reset()
      router.replace(data.default_route || '/')
    },
  }),
  logout: useCall({
    url: '/api/v2/method/logout',
    method: 'POST',
    immediate: false,
    onSuccess() {
      sessionUser.value = getSessionUserFromCookie()
      session.roles = []
      window.location.href = '/login'
    },
  }),
  user: sessionUser,
  roles: [] as string[],
  isLoggedIn: computed(() => sessionUser.value != null),
  hasRole(role: string | string[]) {
    if (Array.isArray(role)) {
      return role.some(r => this.roles.includes(r))
    }
    return this.roles.includes(role)
  },
  isAdmin: computed(() => session.hasRole(['Administrator', 'System Manager', 'Recepcionista']))
}) as any

function getSessionUserFromCookie(): string | null {
  if (typeof document === 'undefined') return null
  
  const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith('user_id='))
    ?.split('=')[1]

  if (!cookieValue || cookieValue === 'Guest') {
    return null
  }
  
  return decodeURIComponent(cookieValue)
}
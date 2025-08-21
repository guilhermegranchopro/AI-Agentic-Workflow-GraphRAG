import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { DarkModeProvider } from '@/lib/ThemeContext'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div id="app-scroll" className="h-screen overflow-auto overscroll-contain">
      <DarkModeProvider>
        <Component {...pageProps} />
      </DarkModeProvider>
    </div>
  )
}

import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { DarkModeProvider } from '@/lib/ThemeContext'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div id="app-scroll">
      <div id="page-shell" className="min-h-full flex flex-col">
        <DarkModeProvider>
          <Component {...pageProps} />
        </DarkModeProvider>
      </div>
    </div>
  )
}

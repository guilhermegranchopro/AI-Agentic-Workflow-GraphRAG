import '@/styles/globals.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div id="app-scroll" className="h-screen overflow-auto overscroll-contain">
      <Component {...pageProps} />
    </div>
  )
}

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/lib/auth-context'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata: Metadata = {
  title: 'FinReportAI - Автоматизированная финансовая отчетность',
  description: 'Облачный сервис для автоматического расчета финансовых показателей малого и среднего бизнеса',
  keywords: 'финансовая отчетность, ROA, ROE, ликвидность, 1С, Excel, автоматизация',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}


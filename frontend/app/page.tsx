/**
 * Landing Page
 * 
 * FR-1.1: Кнопка "Войти через Telegram" на лендинге
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { TelegramLoginButton } from '@/components/telegram-login-button';
import { useAuth } from '@/lib/auth-context';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    // Redirect to dashboard if already authenticated
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <div className="text-xl">Загрузка...</div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl text-center">
        {/* Hero Section */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            FinReportAI
          </h1>
          <p className="text-2xl text-gray-700 mb-2">
            Финансовая отчетность за 5 минут
          </p>
          <p className="text-lg text-gray-600">
            Автоматический расчет 11 ключевых показателей из Excel/1С
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="font-bold text-lg mb-2">11 показателей</h3>
            <p className="text-sm text-gray-600">
              ROA, ROE, ликвидность, маржинальность и другие
            </p>
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="font-bold text-lg mb-2">Быстро</h3>
            <p className="text-sm text-gray-600">
              Загрузил Excel → получил дашборд за 30 секунд
            </p>
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">🔄</div>
            <h3 className="font-bold text-lg mb-2">Интеграция с 1С</h3>
            <p className="text-sm text-gray-600">
              Прямая выгрузка из 1С:Бухгалтерия
            </p>
          </div>
        </div>

        {/* Login Section */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold mb-4">Войти в систему</h2>
          <p className="text-gray-600 mb-6">
            Используйте Telegram для быстрого входа
          </p>
          <TelegramLoginButton />
          <p className="text-xs text-gray-500 mt-4">
            Нажимая кнопку, вы соглашаетесь с условиями использования
          </p>
        </div>

        {/* Pricing Hint */}
        <div className="text-center">
          <p className="text-sm text-gray-600">
            14 дней бесплатно • От 3000₽/месяц • Отмена в любое время
          </p>
        </div>
      </div>
    </main>
  );
}


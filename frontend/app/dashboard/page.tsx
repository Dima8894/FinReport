/**
 * Dashboard Page
 * 
 * Главная страница после авторизации
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-xl">Загрузка...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  async function handleLogout() {
    await logout();
    router.push('/');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">FinReportAI</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-700">
                Привет, <span className="font-medium">{user?.full_name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Выйти
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Добро пожаловать в FinReportAI!
          </h2>
          <p className="text-gray-600">
            Здесь будет ваш дашборд с финансовыми показателями
          </p>
        </div>

        {/* Next Steps */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-bold mb-4">Следующие шаги:</h3>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Создайте профиль компании</li>
            <li>Загрузите финансовые данные (Excel или CSV)</li>
            <li>Получите автоматически рассчитанные показатели</li>
          </ol>
        </div>

        {/* Development Info */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-bold text-blue-900 mb-2">
            🚧 В разработке
          </h3>
          <p className="text-sm text-blue-800">
            Эта страница находится в разработке согласно roadmap Week 1-2.
            Следующие функции будут добавлены в Week 3-4:
          </p>
          <ul className="list-disc list-inside mt-2 text-sm text-blue-800">
            <li>Создание профиля компании</li>
            <li>Загрузка Excel/CSV файлов</li>
            <li>Просмотр финансовых показателей</li>
            <li>Графики и визуализация</li>
          </ul>
        </div>
      </main>
    </div>
  );
}


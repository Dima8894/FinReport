/**
 * Telegram Login Button Component
 * 
 * FR-1.1: Telegram OAuth authentication
 */

'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  auth_date: number;
  hash: string;
}

declare global {
  interface Window {
    TelegramLoginWidget?: {
      dataOnauth?: (user: TelegramUser) => void;
    };
  }
}

export function TelegramLoginButton() {
  const containerRef = useRef<HTMLDivElement>(null);
  const router = useRouter();
  const { login } = useAuth();

  useEffect(() => {
    // Define callback function
    window.TelegramLoginWidget = {
      dataOnauth: async (user: TelegramUser) => {
        console.log('Telegram auth data received:', user);
        
        try {
          await login(user);
          router.push('/dashboard');
        } catch (error) {
          console.error('Login failed:', error);
          alert('Ошибка входа. Попробуйте еще раз.');
        }
      },
    };

    // Load Telegram Widget script
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.async = true;
    script.setAttribute('data-telegram-login', process.env.NEXT_PUBLIC_TELEGRAM_BOT_NAME || 'FinReportAIBot');
    script.setAttribute('data-size', 'large');
    script.setAttribute('data-radius', '10');
    script.setAttribute('data-onauth', 'TelegramLoginWidget.dataOnauth(user)');
    script.setAttribute('data-request-access', 'write');

    if (containerRef.current) {
      containerRef.current.appendChild(script);
    }

    return () => {
      // Cleanup
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
      delete window.TelegramLoginWidget;
    };
  }, [login, router]);

  return (
    <div className="flex justify-center">
      <div ref={containerRef} />
    </div>
  );
}


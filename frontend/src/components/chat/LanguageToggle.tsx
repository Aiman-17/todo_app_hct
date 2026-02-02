/**
 * Language Toggle Component
 *
 * Simple toggle to switch between English and Urdu chatbot responses.
 */

'use client';

import { Languages } from 'lucide-react';

interface LanguageToggleProps {
  language: 'en' | 'ur';
  onLanguageChange: (language: 'en' | 'ur') => void;
}

export function LanguageToggle({ language, onLanguageChange }: LanguageToggleProps) {
  return (
    <div className="flex items-center gap-2 px-3 py-2 bg-white/50 rounded-lg border border-seal-brown/10">
      <Languages className="w-4 h-4 text-seal-brown" />
      <div className="flex gap-1">
        <button
          onClick={() => onLanguageChange('en')}
          className={`
            px-3 py-1 rounded-md text-sm font-medium transition-colors
            ${language === 'en'
              ? 'bg-seal-brown text-white'
              : 'text-seal-brown hover:bg-seal-brown/10'
            }
          `}
          aria-label="Switch to English"
        >
          English
        </button>
        <button
          onClick={() => onLanguageChange('ur')}
          className={`
            px-3 py-1 rounded-md text-sm font-medium transition-colors
            ${language === 'ur'
              ? 'bg-seal-brown text-white'
              : 'text-seal-brown hover:bg-seal-brown/10'
            }
          `}
          aria-label="Switch to Urdu"
          style={{ fontFamily: language === 'ur' ? 'Noto Nastaliq Urdu, sans-serif' : undefined }}
        >
          اردو
        </button>
      </div>
    </div>
  );
}

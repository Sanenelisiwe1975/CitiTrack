import React from 'react';
import { FileText, MapPin, BarChart3, Globe } from 'lucide-react';
import { useTranslation } from '../utils/translations';

const Header = ({ activeTab, setActiveTab, language, setLanguage }) => {
  const { t } = useTranslation(language);

  const tabs = [
    { id: 'report', label: t('report'), icon: FileText },
    { id: 'track', label: t('track'), icon: MapPin },
    { id: 'dashboard', label: t('dashboard'), icon: BarChart3 },
  ];

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'zu', name: 'isiZulu' },
    { code: 'af', name: 'Afrikaans' },
    { code: 'st', name: 'Sesotho' },
  ];

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <MapPin className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">{t('appName')}</h1>
              <p className="text-xs text-gray-500">Civic Issue Tracker</p>
            </div>
          </div>

          {/* Language Selector */}
          <div className="flex items-center space-x-2">
            <Globe className="w-5 h-5 text-gray-500" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 border-b border-gray-200">
          {tabs.map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                  isActive
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};

export default Header;
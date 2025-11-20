import React, { useState, useEffect } from 'react';
import { TrendingUp, CheckCircle, Clock, AlertCircle, BarChart } from 'lucide-react';
import { dashboardAPI } from '../services/api';
import { useTranslation } from '../utils/translations';

const Dashboard = ({ language }) => {
  const { t } = useTranslation(language);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await dashboardAPI.getStats();
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!stats) {
    return <div className="text-center text-gray-500">Failed to load dashboard</div>;
  }

  const statCards = [
    {
      title: 'Total Reports',
      value: stats.summary.total_reports,
      icon: BarChart,
      color: 'bg-blue-500',
    },
    {
      title: 'Pending',
      value: stats.summary.pending,
      icon: Clock,
      color: 'bg-yellow-500',
    },
    {
      title: 'In Progress',
      value: stats.summary.in_progress,
      icon: AlertCircle,
      color: 'bg-orange-500',
    },
    {
      title: 'Resolved',
      value: stats.summary.resolved,
      icon: CheckCircle,
      color: 'bg-green-500',
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">{t('dashboard')}</h2>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
              <p className="text-sm text-gray-600">{stat.title}</p>
            </div>
          );
        })}
      </div>

      {/* Resolution Rate */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Resolution Rate</h3>
          <div className="flex items-center text-green-600">
            <TrendingUp className="w-5 h-5 mr-1" />
            <span className="font-medium">{stats.summary.resolution_rate.toFixed(1)}%</span>
          </div>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-green-500 h-4 rounded-full transition-all duration-500"
            style={{ width: `${stats.summary.resolution_rate}%` }}
          ></div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">By Category</h3>
          <div className="space-y-3">
            {Object.entries(stats.by_category || {}).map(([category, count]) => (
              <div key={category} className="flex justify-between items-center">
                <span className="text-sm text-gray-700 capitalize">{category.replace('_', ' ')}</span>
                <span className="text-sm font-medium text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">By Severity</h3>
          <div className="space-y-3">
            {Object.entries(stats.by_severity || {}).map(([severity, count]) => (
              <div key={severity} className="flex justify-between items-center">
                <span className="text-sm text-gray-700 capitalize">{severity}</span>
                <span className="text-sm font-medium text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
import React, { useState, useEffect } from 'react';
import { WifiOff, RefreshCw } from 'lucide-react';
import { offlineQueue } from '../services/offline';

const OfflineIndicator = () => {
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const updateCount = async () => {
      const count = await offlineQueue.getPendingCount();
      setPendingCount(count);
    };

    updateCount();
    const interval = setInterval(updateCount, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-yellow-50 border-b border-yellow-200">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <WifiOff className="w-5 h-5 text-yellow-600" />
            <div>
              <p className="text-sm font-medium text-yellow-900">
                You are currently offline
              </p>
              <p className="text-xs text-yellow-700">
                {pendingCount > 0
                  ? `${pendingCount} report${pendingCount > 1 ? 's' : ''} queued for submission`
                  : 'Reports will be queued and submitted when online'}
              </p>
            </div>
          </div>
          
          {pendingCount > 0 && (
            <div className="flex items-center space-x-2 text-yellow-700">
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span className="text-sm">Waiting to sync...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OfflineIndicator;
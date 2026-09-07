import React, { useState } from 'react';

function LearningModules({ user }) {
  const [selectedModule, setSelectedModule] = useState(null);

  const modules = [
    {
      id: 'savings',
      title: 'Smart Savings',
      icon: '💰',
      description: 'Learn how to save money effectively',
      lessons: 4,
      duration: '15 min',
      completed: true,
      color: 'green'
    },
    {
      id: 'loans',
      title: 'Understanding Loans',
      icon: '🏦',
      description: 'Everything about loans and interest',
      lessons: 5,
      duration: '20 min',
      completed: true,
      color: 'blue'
    },
    {
      id: 'insurance',
      title: 'Insurance Basics',
      icon: '🛡️',
      description: 'Protect yourself with insurance',
      lessons: 4,
      duration: '15 min',
      completed: false,
      color: 'purple'
    },
    {
      id: 'digital',
      title: 'Digital Banking',
      icon: '📱',
      description: 'Master online and mobile banking',
      lessons: 6,
      duration: '25 min',
      completed: false,
      color: 'orange'
    },
    {
      id: 'schemes',
      title: 'Government Schemes',
      icon: '🏛️',
      description: 'Benefits available for farmers',
      lessons: 5,
      duration: '20 min',
      completed: false,
      color: 'red'
    }
  ];

  const progressData = {
    totalModules: modules.length,
    completedModules: modules.filter(m => m.completed).length,
    points: 450,
    streak: 7
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <span className="text-3xl mr-3">📚</span>
          Financial Literacy Learning
        </h2>
        <p className="text-gray-600">
          Master banking and finance through interactive lessons
        </p>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <StatCard
          icon="📊"
          label="Progress"
          value={`${progressData.completedModules}/${progressData.totalModules}`}
          color="blue"
        />
        <StatCard
          icon="⭐"
          label="Points"
          value={progressData.points}
          color="yellow"
        />
        <StatCard
          icon="🔥"
          label="Streak"
          value={`${progressData.streak} days`}
          color="orange"
        />
        <StatCard
          icon="🎯"
          label="Completion"
          value={`${Math.round((progressData.completedModules / progressData.totalModules) * 100)}%`}
          color="green"
        />
      </div>

      {/* Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map(module => (
          <ModuleCard
            key={module.id}
            module={module}
            onClick={() => setSelectedModule(module)}
          />
        ))}
      </div>

      {/* Achievement Badges */}
      <div className="bg-white rounded-xl shadow-md p-6 mt-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🏆 Your Achievements</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Badge icon="🌟" title="First Steps" subtitle="Complete first module" earned={true} />
          <Badge icon="📖" title="Bookworm" subtitle="Complete 3 modules" earned={true} />
          <Badge icon="🔥" title="Week Streak" subtitle="7 days in a row" earned={true} />
          <Badge icon="🎓" title="Graduate" subtitle="Complete all modules" earned={false} />
        </div>
      </div>

      {/* Leaderboard */}
      <div className="bg-white rounded-xl shadow-md p-6 mt-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🏅 Community Leaderboard</h3>
        <div className="space-y-3">
          {[
            { rank: 1, name: 'राम कुमार', points: 850, avatar: '👨‍🌾', you: true },
            { rank: 2, name: 'सीता देवी', points: 780, avatar: '👩‍🌾' },
            { rank: 3, name: 'मोहन सिंह', points: 720, avatar: '👨‍🌾' },
            { rank: 4, name: 'लक्ष्मी बाई', points: 680, avatar: '👩‍🌾' }
          ].map(entry => (
            <div
              key={entry.rank}
              className={`flex items-center justify-between p-4 rounded-lg ${
                entry.you ? 'bg-green-50 border-2 border-green-500' : 'bg-gray-50'
              }`}
            >
              <div className="flex items-center space-x-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                  entry.rank === 1 ? 'bg-yellow-400 text-yellow-900' :
                  entry.rank === 2 ? 'bg-gray-300 text-gray-700' :
                  entry.rank === 3 ? 'bg-orange-400 text-orange-900' :
                  'bg-gray-200 text-gray-600'
                }`}>
                  #{entry.rank}
                </div>
                <span className="text-2xl">{entry.avatar}</span>
                <div>
                  <p className="font-medium text-gray-800">
                    {entry.name}
                    {entry.you && <span className="ml-2 text-xs bg-green-600 text-white px-2 py-1 rounded">YOU</span>}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-gray-800">{entry.points}</p>
                <p className="text-xs text-gray-500">points</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ module, onClick }) {
  const colorClasses = {
    green: 'from-green-500 to-green-600',
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
    red: 'from-red-500 to-red-600'
  };

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl shadow-md overflow-hidden cursor-pointer hover:shadow-xl transition-all transform hover:-translate-y-1"
    >
      <div className={`bg-gradient-to-br ${colorClasses[module.color]} p-6 text-white`}>
        <div className="text-5xl mb-3">{module.icon}</div>
        <h3 className="text-xl font-bold mb-2">{module.title}</h3>
        <p className="text-sm text-white/80">{module.description}</p>
      </div>
      
      <div className="p-4">
        <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
          <span>📝 {module.lessons} lessons</span>
          <span>⏱️ {module.duration}</span>
        </div>
        
        {module.completed ? (
          <div className="bg-green-50 text-green-800 px-4 py-2 rounded-lg text-center font-medium">
            ✅ Completed
          </div>
        ) : (
          <button className={`w-full bg-gradient-to-r ${colorClasses[module.color]} text-white py-2 rounded-lg hover:opacity-90 transition-all font-medium`}>
            Start Learning →
          </button>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color }) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    yellow: 'from-yellow-500 to-yellow-600',
    orange: 'from-orange-500 to-orange-600',
    green: 'from-green-500 to-green-600'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-xl shadow-md p-4 text-white`}>
      <div className="text-3xl mb-2">{icon}</div>
      <p className="text-sm text-white/80">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}

function Badge({ icon, title, subtitle, earned }) {
  return (
    <div className={`p-4 rounded-xl text-center ${
      earned ? 'bg-yellow-50 border-2 border-yellow-400' : 'bg-gray-100 opacity-50'
    }`}>
      <div className={`text-4xl mb-2 ${earned ? '' : 'grayscale'}`}>{icon}</div>
      <p className="font-bold text-sm text-gray-800">{title}</p>
      <p className="text-xs text-gray-600">{subtitle}</p>
      {!earned && <p className="text-xs text-gray-500 mt-1">🔒 Locked</p>}
    </div>
  );
}

export default LearningModules;

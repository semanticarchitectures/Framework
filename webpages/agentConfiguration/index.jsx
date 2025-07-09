import React, { useState } from 'react';
import { BrainCircuit, Globe, Briefcase, User, Building, ChevronDown, Bot, FileText, Settings, Zap } from 'lucide-react';

// Main App Component
export default function App() {
  const [agentName, setAgentName] = useState('Vermont Destination Expert');
  const [agentDescription, setAgentDescription] = useState('An expert agent for recreational and business travelers interested in Vermont.');
  const [selectedLlm, setSelectedLlm] = useState('gemini-2.0-flash');
  const [activeTab, setActiveTab] = useState('domain');

  // State for Context Configuration
  const [domainKnowledge, setDomainKnowledge] = useState({
    skiResorts: true,
    breweries: true,
    hikingTrails: true,
    mapleSyrupProducers: false,
    historicalSites: true,
    artGalleries: false,
  });

  const [toolAccess, setToolAccess] = useState({
    weatherApi: true,
    flightBooking: true,
    hotelReservations: true,
    restaurantReviews: false,
  });
  
  const [persona, setPersona] = useState("You are a friendly and knowledgeable Vermont travel guide. Your goal is to provide helpful, concise, and inspiring travel advice. You should be enthusiastic and use a slightly informal, conversational tone.");
  const [identity, setIdentity] = useState({
    name: 'Vinnie the Vermonter',
    role: 'Lead Destination Consultant',
    department: 'New England Tourism Bureau',
  });

  const handleDomainKnowledgeChange = (e) => {
    const { name, checked } = e.target;
    setDomainKnowledge(prev => ({ ...prev, [name]: checked }));
  };

  const handleToolAccessChange = (name) => {
    setToolAccess(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const llms = [
    { id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash' },
    { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet' },
    { id: 'llama-3-70b', name: 'Llama 3 70B' },
    { id: 'gpt-4o', name: 'GPT-4o' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'domain':
        return <DomainKnowledgeConfig config={domainKnowledge} handleChange={handleDomainKnowledgeChange} />;
      case 'tools':
        return <ToolAccessConfig config={toolAccess} handleChange={handleToolAccessChange} />;
      case 'persona':
        return <PersonaConfig persona={persona} setPersona={setPersona} />;
      case 'identity':
        return <IdentityConfig identity={identity} setIdentity={setIdentity} />;
      default:
        return null;
    }
  };

  return (
    <div className="bg-slate-50 min-h-screen font-sans text-slate-800">
      <div className="container mx-auto p-4 md:p-8">
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 flex items-center">
            <Bot size={40} className="mr-3 text-blue-600" />
            Agent Configuration
          </h1>
          <p className="text-slate-500 mt-2">Create and configure your AI agents with specialized knowledge and tools.</p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Agent Setup */}
          <div className="lg:col-span-1 flex flex-col gap-8">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xl font-semibold mb-4 text-slate-800 flex items-center"><Settings className="mr-2 text-blue-500"/>Agent Setup</h2>
              <div>
                <label htmlFor="agentName" className="block text-sm font-medium text-slate-600 mb-1">Agent Name</label>
                <input
                  type="text"
                  id="agentName"
                  value={agentName}
                  onChange={(e) => setAgentName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                />
              </div>
              <div className="mt-4">
                <label htmlFor="agentDescription" className="block text-sm font-medium text-slate-600 mb-1">Description</label>
                <textarea
                  id="agentDescription"
                  rows="3"
                  value={agentDescription}
                  onChange={(e) => setAgentDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                />
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xl font-semibold mb-4 text-slate-800 flex items-center"><BrainCircuit className="mr-2 text-blue-500"/>Language Model</h2>
              <p className="text-sm text-slate-500 mb-3">Select the core LLM for your agent.</p>
              <div className="relative">
                <select
                  value={selectedLlm}
                  onChange={(e) => setSelectedLlm(e.target.value)}
                  className="w-full appearance-none bg-slate-50 border border-slate-300 rounded-lg px-4 py-3 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                >
                  {llms.map(llm => (
                    <option key={llm.id} value={llm.id}>{llm.name}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              </div>
            </div>
          </div>

          {/* Right Column: Context Configuration */}
          <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4 text-slate-800">Context Configuration</h2>
            <div className="border-b border-slate-200">
              <nav className="-mb-px flex space-x-6">
                <TabButton title="Domain Knowledge" icon={<FileText size={16}/>} isActive={activeTab === 'domain'} onClick={() => setActiveTab('domain')} />
                <TabButton title="Tool Access" icon={<Zap size={16}/>} isActive={activeTab === 'tools'} onClick={() => setActiveTab('tools')} />
                <TabButton title="Persona" icon={<User size={16}/>} isActive={activeTab === 'persona'} onClick={() => setActiveTab('persona')} />
                <TabButton title="Identity" icon={<Building size={16}/>} isActive={activeTab === 'identity'} onClick={() => setActiveTab('identity')} />
              </nav>
            </div>
            <div className="mt-6">
              {renderContent()}
            </div>
          </div>
        </main>
        
        <footer className="mt-8 flex justify-end">
            <button className="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors shadow focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Save Agent Configuration
            </button>
        </footer>
      </div>
    </div>
  );
}

// Tab Button Component
const TabButton = ({ title, icon, isActive, onClick }) => (
  <button
    onClick={onClick}
    className={`flex items-center space-x-2 px-1 py-3 text-sm font-medium transition-colors ${
      isActive
        ? 'border-b-2 border-blue-600 text-blue-600'
        : 'border-b-2 border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
    }`}
  >
    {icon}
    <span>{title}</span>
  </button>
);

// Domain Knowledge Configuration Component
const DomainKnowledgeConfig = ({ config, handleChange }) => (
  <div>
    <h3 className="text-lg font-semibold text-slate-700 mb-1">Vermont Domain Information</h3>
    <p className="text-sm text-slate-500 mb-4">Select knowledge sources to ground the agent's responses.</p>
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <Checkbox label="Ski Resorts & Conditions" name="skiResorts" checked={config.skiResorts} onChange={handleChange} />
      <Checkbox label="Breweries & Wineries" name="breweries" checked={config.breweries} onChange={handleChange} />
      <Checkbox label="Hiking Trails & Parks" name="hikingTrails" checked={config.hikingTrails} onChange={handleChange} />
      <Checkbox label="Maple Syrup Producers" name="mapleSyrupProducers" checked={config.mapleSyrupProducers} onChange={handleChange} />
      <Checkbox label="Historical Sites" name="historicalSites" checked={config.historicalSites} onChange={handleChange} />
      <Checkbox label="Art Galleries & Museums" name="artGalleries" checked={config.artGalleries} onChange={handleChange} />
    </div>
  </div>
);

// Custom Checkbox Component
const Checkbox = ({ label, name, checked, onChange }) => (
  <label className="flex items-center p-3 bg-slate-50 rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors cursor-pointer">
    <input
      type="checkbox"
      name={name}
      checked={checked}
      onChange={onChange}
      className="h-5 w-5 rounded border-slate-400 text-blue-600 focus:ring-blue-500"
    />
    <span className="ml-3 text-sm font-medium text-slate-700">{label}</span>
  </label>
);

// Tool Access Configuration Component
const ToolAccessConfig = ({ config, handleChange }) => (
  <div>
    <h3 className="text-lg font-semibold text-slate-700 mb-1">Web App & API Access</h3>
    <p className="text-sm text-slate-500 mb-4">Enable tools to allow the agent to perform actions and access live data.</p>
    <div className="space-y-4">
      <Toggle label="Weather API" description="Access real-time weather forecasts." enabled={config.weatherApi} onToggle={() => handleChange('weatherApi')} />
      <Toggle label="Flight Booking System" description="Search for and book flights." enabled={config.flightBooking} onToggle={() => handleChange('flightBooking')} />
      <Toggle label="Hotel Reservation API" description="Find and reserve accommodations." enabled={config.hotelReservations} onToggle={() => handleChange('hotelReservations')} />
      <Toggle label="Restaurant Review Aggregator" description="Access local dining reviews and ratings." enabled={config.restaurantReviews} onToggle={() => handleChange('restaurantReviews')} />
    </div>
  </div>
);

// Custom Toggle Component
const Toggle = ({ label, description, enabled, onToggle }) => (
    <div 
        onClick={onToggle}
        className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors cursor-pointer"
    >
        <div>
            <p className="font-medium text-slate-700">{label}</p>
            <p className="text-xs text-slate-500">{description}</p>
        </div>
        <div className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${enabled ? 'bg-blue-600' : 'bg-slate-300'}`}>
            <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${enabled ? 'translate-x-6' : ''}`}></div>
        </div>
    </div>
);

// Persona Configuration Component
const PersonaConfig = ({ persona, setPersona }) => (
  <div>
    <h3 className="text-lg font-semibold text-slate-700 mb-1">Agent Persona & Role Prompts</h3>
    <p className="text-sm text-slate-500 mb-4">Define the agent's personality, tone, and core instructions.</p>
    <textarea
      rows="8"
      value={persona}
      onChange={(e) => setPersona(e.target.value)}
      className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
      placeholder="e.g., You are a helpful assistant..."
    />
  </div>
);

// Identity Configuration Component
const IdentityConfig = ({ identity, setIdentity }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setIdentity(prev => ({...prev, [name]: value}));
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-slate-700 mb-1">Organizational Identity</h3>
      <p className="text-sm text-slate-500 mb-4">Define the agent's identity within your organization.</p>
      <div className="space-y-4">
        <div>
          <label htmlFor="identityName" className="block text-sm font-medium text-slate-600 mb-1">Agent's Name</label>
          <input type="text" id="identityName" name="name" value={identity.name} onChange={handleChange} className="w-full sm:w-2/3 px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" />
        </div>
        <div>
          <label htmlFor="identityRole" className="block text-sm font-medium text-slate-600 mb-1">Role</label>
          <input type="text" id="identityRole" name="role" value={identity.role} onChange={handleChange} className="w-full sm:w-2/3 px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" />
        </div>
        <div>
          <label htmlFor="identityDepartment" className="block text-sm font-medium text-slate-600 mb-1">Department / Group</label>
          <input type="text" id="identityDepartment" name="department" value={identity.department} onChange={handleChange} className="w-full sm:w-2/3 px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" />
        </div>
      </div>
    </div>
  );
};


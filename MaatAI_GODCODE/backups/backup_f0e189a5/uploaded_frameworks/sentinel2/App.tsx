
import React, { useState } from 'react';
import Layout from './components/Layout';
import ForensicTerminal from './components/ForensicTerminal';
import RefractalVisualizer from './components/RefractalVisualizer';
import SentinelMonitor from './components/SentinelMonitor';
import GrandRegister from './components/GrandRegister';
import HybridThinking from './components/HybridThinking';
import TaskManager from './components/TaskManager';
import FileVault from './components/FileVault';
import SelfDiagnostic from './components/SelfDiagnostic';
import { UISection } from './types';

const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState<UISection>(UISection.FORENSIC_TERMINAL);

  const renderSection = () => {
    switch (activeSection) {
      case UISection.FORENSIC_TERMINAL:
        return <ForensicTerminal />;
      case UISection.TASK_MANAGER:
        return <TaskManager />;
      case UISection.FILE_VAULT:
        return <FileVault />;
      case UISection.HYBRID_THINKING:
        return <HybridThinking />;
      case UISection.SELF_DIAGNOSTIC:
        return <SelfDiagnostic />;
      case UISection.REFRACTAL_GRAPH:
        return <RefractalVisualizer />;
      case UISection.SENTINEL_MONITOR:
        return <SentinelMonitor />;
      case UISection.GRAND_REGISTER:
        return <GrandRegister />;
      default:
        return <ForensicTerminal />;
    }
  };

  return (
    <Layout activeSection={activeSection} setActiveSection={setActiveSection}>
      {renderSection()}
    </Layout>
  );
};

export default App;

/**
 * Niveau 2 (`02-features/acp-pilot-panel/AcpPilotPanel.tsx`)
 * Orchestrateur visuel léger (< 140 lignes) assemblant les partials ChatKit / assistant-ui.
 */
import React from 'react';
import { useAcpPilotController } from './useAcpPilotController';
import { PilotHeaderBarPartial } from './partials/PilotHeaderBarPartial';
import { PilotMessageStreamPartial } from './partials/PilotMessageStreamPartial';
import { PilotInputQuickChipsPartial } from './partials/PilotInputQuickChipsPartial';

export interface AcpPilotPanelProps {
  title?: string;
  sessionId?: string;
  quickChips?: string[];
}

export const AcpPilotPanel: React.FC<AcpPilotPanelProps> = ({
  title = 'Assistant IA (ACP · Google ADK · ChatKit)',
  sessionId = 'sess-ui-001',
  quickChips = ['Analyser la maquette', 'Générer le rapport', 'Vérifier la conformité'],
}) => {
  const controller = useAcpPilotController(sessionId);

  return (
    <aside className="flex flex-col h-full w-full bg-slate-900 border-l border-slate-800 text-slate-100">
      <PilotHeaderBarPartial
        title={title}
        sessionId={controller.sessionId}
        transportMode={controller.transportMode}
        onChangeTransport={controller.setTransportMode}
      />
      <PilotMessageStreamPartial
        messages={controller.messages}
        isStreaming={controller.isStreaming}
      />
      <PilotInputQuickChipsPartial
        inputDraft={controller.inputDraft}
        onChangeInput={controller.setInputDraft}
        onSend={controller.sendMessage}
        quickChips={quickChips}
        disabled={controller.isStreaming}
      />
    </aside>
  );
};

/**
 * Niveau 2 (`02-features/acp-pilot-panel/`) — Custom Hook Contrôleur
 * Pilote le panneau de chat IA (OpenAI ChatKit / assistant-ui) via ACP ou Google ADK.
 */
import { useState, useCallback } from 'react';
import { AcpMessage, AcpProtocolClient } from '../../sdk/acp/acpClient';

export type AgentTransportMode = 'ACP' | 'GOOGLE_ADK' | 'OPENAI_CHATKIT';

export function useAcpPilotController(initialSessionId: string = 'sess-ui-001') {
  const [sessionId] = useState<string>(initialSessionId);
  const [transportMode, setTransportMode] = useState<AgentTransportMode>('ACP');
  const [messages, setMessages] = useState<AcpMessage[]>([]);
  const [inputDraft, setInputDraft] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);

  const acpClient = new AcpProtocolClient();

  const sendMessage = useCallback(async (textOverride?: string) => {
    const prompt = (textOverride ?? inputDraft).trim();
    if (!prompt) return;

    const userMsg: AcpMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: prompt,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputDraft('');
    setIsStreaming(true);

    try {
      const reply = await acpClient.executeRun({
        agentName: 'snorbik-orchestrator',
        sessionId,
        input: prompt,
        context: { transportMode },
      });
      setMessages((prev) => [...prev, reply]);
    } finally {
      setIsStreaming(false);
    }
  }, [inputDraft, sessionId, transportMode]);

  return {
    sessionId,
    transportMode,
    setTransportMode,
    messages,
    inputDraft,
    setInputDraft,
    isStreaming,
    sendMessage,
  };
}

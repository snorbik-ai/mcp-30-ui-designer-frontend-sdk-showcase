/**
 * Snorbik Frontend UI SDK — Client Standard ACP (Agent Communication Protocol)
 * Compatible avec OpenAI ChatKit (@openai/chatkit-react), assistant-ui et AG-UI.
 */

export interface AcpToolCallEvent {
  toolName: string;
  arguments: Record<string, unknown>;
  resultJson?: Record<string, unknown>;
  status: 'running' | 'completed' | 'failed';
}

export interface AcpMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  toolCalls?: AcpToolCallEvent[];
}

export interface AcpRunRequest {
  agentName: string;
  sessionId: string;
  input: string;
  attachments?: string[];
  context?: Record<string, unknown>;
}

export class AcpProtocolClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string = '/api/acp/v1') {
    this.baseUrl = baseUrl;
  }

  async executeRun(req: AcpRunRequest): Promise<AcpMessage> {
    const response = await fetch(`${this.baseUrl}/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });

    if (!response.ok) {
      throw new Error(`ACP Error HTTP ${response.status}`);
    }

    return (await response.json()) as AcpMessage;
  }
}

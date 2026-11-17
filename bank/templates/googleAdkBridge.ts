/**
 * Snorbik Frontend UI SDK — Connecteur Direct Google ADK (Agent Development Kit)
 * Branche directement l'interface React sur un runner `google-adk` (/run_sse).
 */

export interface GoogleAdkConfig {
  adkBaseUrl: string;
  appName: string;
  userId: string;
}

export interface GoogleAdkEvent {
  author: string;
  content?: {
    parts?: Array<{ text?: string; functionCall?: Record<string, unknown>; functionResponse?: Record<string, unknown> }>;
  };
  partial?: boolean;
}

export class GoogleAdkBridge {
  private readonly config: GoogleAdkConfig;

  constructor(config: GoogleAdkConfig) {
    this.config = config;
  }

  async ensureSession(sessionId: string): Promise<string> {
    const { adkBaseUrl, appName, userId } = this.config;
    const url = `${adkBaseUrl}/apps/${appName}/users/${userId}/sessions/${sessionId}`;
    await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    return sessionId;
  }

  async sendPrompt(sessionId: string, promptText: string): Promise<GoogleAdkEvent[]> {
    const { adkBaseUrl, appName, userId } = this.config;
    const response = await fetch(`${adkBaseUrl}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        app_name: appName,
        user_id: userId,
        session_id: sessionId,
        new_message: { role: 'user', parts: [{ text: promptText }] },
      }),
    });
    if (!response.ok) {
      throw new Error(`Google ADK Runner HTTP ${response.status}`);
    }
    return (await response.json()) as GoogleAdkEvent[];
  }
}

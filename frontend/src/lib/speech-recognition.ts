/**
 * Speech Recognition Wrapper for Web Speech API
 *
 * Provides a clean interface to the browser's speech recognition capabilities
 * with proper error handling and browser compatibility checks.
 */

interface SpeechRecognitionConfig {
  language?: string;
  continuous?: boolean;
  interimResults?: boolean;
  maxAlternatives?: number;
}

interface SpeechRecognitionResult {
  transcript: string;
  confidence: number;
  isFinal: boolean;
}

export class SpeechRecognitionService {
  private recognition: any;
  private isListening: boolean = false;
  private onResultCallback?: (result: SpeechRecognitionResult) => void;
  private onErrorCallback?: (error: string) => void;
  private onEndCallback?: () => void;

  constructor(config: SpeechRecognitionConfig = {}) {
    // SSR guard - only initialize in browser
    if (typeof window === 'undefined') {
      return;
    }

    // Check browser support
    if (!this.isSupported()) {
      console.warn('Speech recognition not supported in this browser');
      return;
    }

    // Initialize speech recognition
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();

    // Configure recognition
    this.recognition.lang = config.language || 'en-US';
    this.recognition.continuous = config.continuous || false;
    this.recognition.interimResults = config.interimResults || true;
    this.recognition.maxAlternatives = config.maxAlternatives || 1;

    // Setup event handlers
    this.setupEventHandlers();
  }

  /**
   * Check if speech recognition is supported in the current browser
   */
  isSupported(): boolean {
    // SSR guard
    if (typeof window === 'undefined') {
      return false;
    }
    return !!(window as any).SpeechRecognition || !!(window as any).webkitSpeechRecognition;
  }

  /**
   * Start listening for speech input
   */
  start(): Promise<string> {
    if (!this.isSupported()) {
      return Promise.reject(new Error('Speech recognition not supported'));
    }

    if (this.isListening) {
      return Promise.reject(new Error('Already listening'));
    }

    return new Promise((resolve, reject) => {
      let finalTranscript = '';

      this.onResultCallback = (result) => {
        if (result.isFinal) {
          finalTranscript = result.transcript;
        }
      };

      this.onErrorCallback = (error) => {
        reject(new Error(error));
      };

      this.onEndCallback = () => {
        this.isListening = false;
        if (finalTranscript) {
          resolve(finalTranscript);
        } else {
          reject(new Error('No speech detected'));
        }
      };

      try {
        this.recognition.start();
        this.isListening = true;
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Stop listening for speech input
   */
  stop(): void {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }

  /**
   * Abort speech recognition
   */
  abort(): void {
    if (this.recognition && this.isListening) {
      this.recognition.abort();
      this.isListening = false;
    }
  }

  /**
   * Get current listening state
   */
  getIsListening(): boolean {
    return this.isListening;
  }

  /**
   * Setup event handlers for speech recognition
   */
  private setupEventHandlers(): void {
    if (!this.recognition) return;

    // Handle recognition results
    this.recognition.onresult = (event: any) => {
      const results = event.results;
      const lastResult = results[results.length - 1];
      const transcript = lastResult[0].transcript;
      const confidence = lastResult[0].confidence;
      const isFinal = lastResult.isFinal;

      if (this.onResultCallback) {
        this.onResultCallback({ transcript, confidence, isFinal });
      }
    };

    // Handle errors
    this.recognition.onerror = (event: any) => {
      let errorMessage = 'Speech recognition error';

      switch (event.error) {
        case 'no-speech':
          errorMessage = 'No speech detected. Please try speaking again.';
          break;
        case 'audio-capture':
          errorMessage = 'Cannot access microphone. Please check your microphone is connected and not in use by another app.';
          break;
        case 'not-allowed':
          errorMessage = 'Microphone permission denied. Please allow microphone access in your browser settings.';
          break;
        case 'network':
          errorMessage = 'Network error. Speech recognition requires internet connection.';
          break;
        case 'aborted':
          // Silent abort, user clicked stop
          errorMessage = '';
          break;
        default:
          errorMessage = `Speech recognition error: ${event.error}`;
      }

      if (this.onErrorCallback && errorMessage) {
        this.onErrorCallback(errorMessage);
      }
    };

    // Handle recognition end
    this.recognition.onend = () => {
      this.isListening = false;
      if (this.onEndCallback) {
        this.onEndCallback();
      }
    };

    // Handle recognition start
    this.recognition.onstart = () => {
      this.isListening = true;
    };
  }

  /**
   * Request microphone permission
   * Note: Speech Recognition API handles permissions automatically
   * This is a placeholder for UX flow
   */
  static async requestPermission(): Promise<boolean> {
    // Speech Recognition API will request permission on first start()
    // Just return true to allow the UX flow to proceed
    return true;
  }

  /**
   * Check if microphone permission has been granted
   */
  static async checkPermission(): Promise<PermissionState> {
    // SSR guard
    if (typeof window === 'undefined' || typeof navigator === 'undefined') {
      return 'prompt';
    }

    try {
      const result = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      return result.state;
    } catch (error) {
      // Permissions API not supported, assume prompt state
      // Speech Recognition will handle permission request
      return 'prompt';
    }
  }

  /**
   * Get list of available languages for speech recognition
   */
  static getSupportedLanguages(): string[] {
    return [
      'en-US', // English (United States)
      'en-GB', // English (United Kingdom)
      'es-ES', // Spanish (Spain)
      'fr-FR', // French (France)
      'de-DE', // German (Germany)
      'it-IT', // Italian (Italy)
      'ja-JP', // Japanese (Japan)
      'ko-KR', // Korean (Korea)
      'zh-CN', // Chinese (Simplified)
      'ar-SA', // Arabic (Saudi Arabia)
      'ur-PK', // Urdu (Pakistan)
    ];
  }
}

/**
 * Create a new speech recognition instance with default settings
 */
export function createSpeechRecognition(config?: SpeechRecognitionConfig): SpeechRecognitionService {
  return new SpeechRecognitionService(config);
}

/**
 * Quick helper to get a single voice input
 */
export async function getVoiceInput(language: string = 'en-US'): Promise<string> {
  const recognition = createSpeechRecognition({ language });
  return recognition.start();
}

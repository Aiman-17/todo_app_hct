/**
 * React Hook for Speech Recognition
 *
 * Provides a simple React interface to the Web Speech API with state management.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { SpeechRecognitionService } from '@/lib/speech-recognition';

interface UseSpeechRecognitionOptions {
  language?: string;
  continuous?: boolean;
  interimResults?: boolean;
  onTranscript?: (transcript: string, isFinal: boolean) => void;
  onError?: (error: string) => void;
}

interface UseSpeechRecognitionReturn {
  isListening: boolean;
  isSupported: boolean;
  transcript: string;
  interimTranscript: string;
  error: string | null;
  start: () => void;
  stop: () => void;
  resetTranscript: () => void;
}

export function useSpeechRecognition(
  options: UseSpeechRecognitionOptions = {}
): UseSpeechRecognitionReturn {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);

  const recognitionRef = useRef<SpeechRecognitionService | null>(null);
  const finalTranscriptRef = useRef('');

  // Initialize speech recognition on mount (client-side only)
  useEffect(() => {
    // SSR guard - only run in browser
    if (typeof window === 'undefined') {
      return;
    }

    const recognition = new SpeechRecognitionService({
      language: options.language || 'en-US',
      continuous: options.continuous || false,
      interimResults: options.interimResults !== false, // Default to true
    });

    setIsSupported(recognition.isSupported());
    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [options.language, options.continuous, options.interimResults]);

  /**
   * Start listening for speech input
   */
  const start = useCallback(() => {
    if (!recognitionRef.current || !isSupported) {
      const errorMsg = 'Speech recognition not supported in this browser';
      setError(errorMsg);
      if (options.onError) {
        options.onError(errorMsg);
      }
      return;
    }

    if (isListening) {
      return; // Already listening
    }

    // Reset state
    setError(null);
    setTranscript('');
    setInterimTranscript('');
    finalTranscriptRef.current = '';

    recognitionRef.current.start()
      .then((finalTranscript) => {
        setTranscript(finalTranscript);
        finalTranscriptRef.current = finalTranscript;
        setIsListening(false);

        if (options.onTranscript) {
          options.onTranscript(finalTranscript, true);
        }
      })
      .catch((err) => {
        const errorMsg = err.message || 'Speech recognition failed';
        setError(errorMsg);
        setIsListening(false);

        if (options.onError) {
          options.onError(errorMsg);
        }
      });

    setIsListening(true);
  }, [isSupported, isListening, options]);

  /**
   * Stop listening for speech input
   */
  const stop = useCallback(() => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, [isListening]);

  /**
   * Reset transcript to empty string
   */
  const resetTranscript = useCallback(() => {
    setTranscript('');
    setInterimTranscript('');
    finalTranscriptRef.current = '';
    setError(null);
  }, []);

  return {
    isListening,
    isSupported,
    transcript,
    interimTranscript,
    error,
    start,
    stop,
    resetTranscript,
  };
}

/**
 * Hook for one-time voice input (simplified version)
 */
export function useVoiceInput(
  onTranscript: (transcript: string) => void,
  language: string = 'en-US'
) {
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(false);

  // Use lazy initialization to avoid SSR issues
  const recognition = useRef<SpeechRecognitionService | null>(null);

  // Initialize on mount (client-side only)
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    recognition.current = new SpeechRecognitionService({ language });
    setIsSupported(recognition.current.isSupported());
  }, [language]);

  const startListening = useCallback(() => {
    if (!recognition.current || !isSupported) {
      setError('Speech recognition not available');
      return;
    }

    setError(null);
    setIsListening(true);

    recognition.current.start()
      .then((transcript) => {
        onTranscript(transcript);
        setIsListening(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsListening(false);
      });
  }, [onTranscript, isSupported]);

  const stopListening = useCallback(() => {
    if (recognition.current) {
      recognition.current.stop();
    }
    setIsListening(false);
  }, []);

  return {
    isListening,
    error,
    startListening,
    stopListening,
    isSupported,
  };
}

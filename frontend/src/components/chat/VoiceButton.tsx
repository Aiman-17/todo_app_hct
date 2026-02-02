/**
 * Voice Button Component
 *
 * Microphone button for voice input in chat interface.
 * Handles microphone permissions, recording state, and error feedback.
 */

'use client';

import { useState, useEffect } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import { useVoiceInput } from '@/hooks/useSpeechRecognition';
import { SpeechRecognitionService } from '@/lib/speech-recognition';

interface VoiceButtonProps {
  onTranscript: (transcript: string) => void;
  language?: string;
  disabled?: boolean;
  className?: string;
}

export function VoiceButton({
  onTranscript,
  language = 'en-US',
  disabled = false,
  className = '',
}: VoiceButtonProps) {
  const [showPermissionPrompt, setShowPermissionPrompt] = useState(false);

  const {
    isListening,
    error,
    startListening,
    stopListening,
    isSupported,
  } = useVoiceInput(onTranscript, language);

  const handleClick = async () => {
    if (disabled) return;

    // If already listening, stop
    if (isListening) {
      stopListening();
      return;
    }

    // Start listening - Speech Recognition API handles permissions
    startListening();
  };

  // Show error notification and permission prompt if needed
  useEffect(() => {
    if (error) {
      console.error('Voice input error:', error);

      // Show permission prompt for permission-related errors
      if (error.includes('permission') || error.includes('not-allowed')) {
        setShowPermissionPrompt(true);
      }
    }
  }, [error]);

  // Don't render if not supported
  if (!isSupported) {
    return null;
  }

  const buttonClasses = `
    relative inline-flex items-center justify-center
    w-10 h-10 rounded-full
    transition-all duration-200 ease-in-out
    focus:outline-none focus:ring-2 focus:ring-offset-2
    ${isListening
      ? 'bg-red-500 hover:bg-red-600 focus:ring-red-500 animate-pulse'
      : 'bg-[#2D0B00] hover:bg-[#3D1500] focus:ring-[#2D0B00]'
    }
    ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
    ${className}
  `;

  return (
    <>
      <button
        type="button"
        onClick={handleClick}
        disabled={disabled}
        className={buttonClasses}
        title={isListening ? 'Stop recording' : 'Start voice input'}
        aria-label={isListening ? 'Stop recording' : 'Start voice input'}
      >
        {isListening ? (
          <>
            {/* Pulsing ring animation */}
            <span className="absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75 animate-ping" />
            <Mic className="w-5 h-5 text-white relative z-10" />
          </>
        ) : (
          <Mic className="w-5 h-5 text-white" />
        )}
      </button>

      {/* Permission Prompt Modal */}
      {showPermissionPrompt && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md mx-4 shadow-xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-red-100 rounded-full">
                <MicOff className="w-6 h-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-[#2D0B00]">
                Microphone Permission Required
              </h3>
            </div>

            <p className="text-gray-600 mb-4">
              To use voice input, please allow microphone access in your browser settings.
            </p>

            <div className="bg-gray-50 rounded-md p-4 mb-4">
              <p className="text-sm text-gray-700 font-medium mb-2">How to enable:</p>
              <ol className="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                <li>Click the microphone icon in your browser's address bar</li>
                <li>Select "Allow" for microphone access</li>
                <li>Try voice input again</li>
              </ol>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowPermissionPrompt(false)}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  setShowPermissionPrompt(false);
                  // Try again - Speech Recognition API will re-request permission
                  startListening();
                }}
                className="flex-1 px-4 py-2 bg-[#2D0B00] text-white rounded-md hover:bg-[#3D1500] transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Recording Indicator */}
      {isListening && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-red-500 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-3 animate-fade-in">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span className="font-medium">Listening...</span>
            <button
              onClick={stopListening}
              className="ml-2 px-3 py-1 bg-white bg-opacity-20 rounded-full hover:bg-opacity-30 transition-colors"
            >
              Stop
            </button>
          </div>
        </div>
      )}

      {/* Error Notification */}
      {error && !isListening && (
        <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3 animate-fade-in max-w-md">
            <MicOff className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm">{error}</p>
            <button
              onClick={() => {
                // Clear error by attempting to start again
                handleClick();
              }}
              className="ml-2 px-3 py-1 bg-white bg-opacity-20 rounded-md hover:bg-opacity-30 transition-colors text-sm"
            >
              Retry
            </button>
          </div>
        </div>
      )}
    </>
  );
}

/**
 * Voice Input Indicator (for showing transcription in progress)
 */
interface VoiceInputIndicatorProps {
  transcript: string;
  isListening: boolean;
}

export function VoiceInputIndicator({ transcript, isListening }: VoiceInputIndicatorProps) {
  if (!isListening && !transcript) return null;

  return (
    <div className="absolute bottom-full mb-2 left-0 right-0 px-4">
      <div className="bg-white border-2 border-[#2D0B00] rounded-lg p-3 shadow-lg">
        <div className="flex items-center gap-2 mb-1">
          <div className="flex gap-1">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse delay-75" />
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse delay-150" />
          </div>
          <span className="text-xs font-medium text-[#2D0B00]">
            {isListening ? 'Listening...' : 'Done'}
          </span>
        </div>
        {transcript && (
          <p className="text-sm text-gray-700 italic">"{transcript}"</p>
        )}
      </div>
    </div>
  );
}

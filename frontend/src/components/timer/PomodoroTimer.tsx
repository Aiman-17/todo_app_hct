"use client";

/**
 * Pomodoro Timer Component
 *
 * Focus timer with circular countdown visualization.
 * Features:
 * - Circular progress countdown
 * - Duration presets (5, 10, 20, 25, 60, 120 minutes)
 * - Start/Pause/Stop controls
 * - Visual and audio notifications
 * - Task focus integration
 */

import { useState, useEffect, useRef } from "react";
import { Play, Pause, RotateCcw } from "lucide-react";

interface PomodoroTimerProps {
  onComplete?: () => void;
  taskName?: string;
}

const DURATION_PRESETS = [
  { value: 5, label: "5" },
  { value: 10, label: "10" },
  { value: 20, label: "20" },
  { value: 25, label: "25" },
  { value: 60, label: "60" },
  { value: 120, label: "120" },
];

export function PomodoroTimer({ onComplete, taskName }: PomodoroTimerProps) {
  const [selectedDuration, setSelectedDuration] = useState(25); // minutes
  const [timeLeft, setTimeLeft] = useState(selectedDuration * 60); // seconds
  const [isRunning, setIsRunning] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const totalSeconds = selectedDuration * 60;
  const progress = ((totalSeconds - timeLeft) / totalSeconds) * 100;

  // Calculate circle properties
  const size = 240;
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  // Timer logic

  useEffect(() => {
  if (!isRunning) {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    return;
  }

  intervalRef.current = setInterval(() => {
    setTimeLeft((prev) => {
      if (prev <= 1) {
        clearInterval(intervalRef.current!);
        intervalRef.current = null;
        setIsRunning(false);
        setIsCompleted(true);
        onComplete?.();
        return 0;
      }
      return prev - 1;
    });
  }, 1000);

  return () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };
}, [isRunning, onComplete]);


  // useEffect(() => {
  //   if (isRunning && timeLeft > 0) {
  //     intervalRef.current = setInterval(() => {
  //       setTimeLeft((prev) => {
  //         if (prev <= 1) {
  //           setIsRunning(false);
  //           setIsCompleted(true);
  //           onComplete?.();
  //           // Play notification sound (optional)
  //           return 0;
  //         }
  //         return prev - 1;
  //       });
  //     }, 1000);
  //   } else {
  //     if (intervalRef.current) {
  //       clearInterval(intervalRef.current);
  //     }
  //   }

  //   return () => {
  //     if (intervalRef.current) {
  //       clearInterval(intervalRef.current);
  //     }
  //   };
  // }, [isRunning, timeLeft, onComplete]);

  const handleStart = () => {
    setIsRunning(true);
    setIsCompleted(false);
  };

  const handlePause = () => {
    setIsRunning(false);
  };

  const handleReset = () => {
    setIsRunning(false);
    setTimeLeft(selectedDuration * 60);
    setIsCompleted(false);
  };

  const handleDurationChange = (minutes: number) => {
    setSelectedDuration(minutes);
    setTimeLeft(minutes * 60);
    setIsRunning(false);
    setIsCompleted(false);
  };

  return (
    <div className="bg-white rounded-3xl p-8 shadow-lg">
      {/* Header */}
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-seal-brown mb-2">
          {isCompleted ? "Time's Up!" : "Focus Time"}
        </h2>
        {taskName && (
          <p className="text-sm text-seal-brown/60">
            Working on: {taskName}
          </p>
        )}
      </div>

      {/* Circular Timer */}
      <div className="relative flex items-center justify-center mb-8">
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#E0E0E0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />

          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#42A5F5"
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-300 ease-linear"
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-5xl font-bold text-seal-brown mb-2">
            {formatTime(timeLeft)}
          </div>
          {isCompleted && (
            <div className="text-sm text-green-600 font-medium">
              Great work! 🎉
            </div>
          )}
        </div>
      </div>

      {/* Duration Presets */}
      {!isRunning && (
        <div className="flex items-center justify-center gap-2 mb-6">
          {DURATION_PRESETS.map((preset) => (
            <button
              key={preset.value}
              onClick={() => handleDurationChange(preset.value)}
              className={`
                px-4 py-2 rounded-lg text-sm font-medium
                transition-all duration-200
                ${
                  selectedDuration === preset.value
                    ? "bg-seal-brown text-rose-white shadow-md"
                    : "bg-rose-white text-seal-brown hover:bg-seal-brown/10"
                }
              `}
            >
              {preset.label}
            </button>
          ))}
        </div>
      )}

      {/* Controls */}
      <div className="flex items-center justify-center gap-4">
        {!isRunning ? (
          <button
            onClick={handleStart}
            disabled={timeLeft === 0}
            className="
              px-8 py-4 rounded-full
              bg-seal-brown text-rose-white
              hover:bg-seal-brown/90
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-all duration-200
              flex items-center gap-2
              font-medium shadow-lg
            "
          >
            <Play className="w-5 h-5" />
            {timeLeft === selectedDuration * 60 ? "Start Focus" : "Resume"}
          </button>
        ) : (
          <button
            onClick={handlePause}
            className="
              px-8 py-4 rounded-full
              bg-orange-500 text-white
              hover:bg-orange-600
              transition-all duration-200
              flex items-center gap-2
              font-medium shadow-lg
            "
          >
            <Pause className="w-5 h-5" />
            Pause
          </button>
        )}

        <button
          onClick={handleReset}
          className="
            p-4 rounded-full
            bg-rose-white text-seal-brown
            hover:bg-seal-brown/10
            transition-all duration-200
            shadow-md
          "
          aria-label="Reset timer"
        >
          <RotateCcw className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}

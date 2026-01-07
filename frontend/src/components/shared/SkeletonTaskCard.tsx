/**
 * Skeleton Task Card Component
 *
 * Loading placeholder for task cards with shimmer animation.
 * Provides better UX than spinners by showing the expected layout.
 */

export function SkeletonTaskCard() {
  return (
    <div className="relative flex items-center gap-4 p-4 rounded-2xl shadow-md bg-gray-100 animate-pulse">
      {/* Checkbox Skeleton */}
      <div className="flex-shrink-0 w-11 h-11 rounded-lg bg-gray-200" />

      {/* Content Skeleton */}
      <div className="flex-1 min-w-0 space-y-2">
        {/* Title Skeleton */}
        <div className="h-4 bg-gray-200 rounded w-3/4" />

        {/* Description Skeleton */}
        <div className="h-3 bg-gray-200 rounded w-1/2" />

        {/* Tags Skeleton */}
        <div className="flex gap-1">
          <div className="h-5 w-16 bg-gray-200 rounded-full" />
          <div className="h-5 w-20 bg-gray-200 rounded-full" />
        </div>
      </div>

      {/* Action Buttons Skeleton */}
      <div className="flex items-center gap-2">
        <div className="w-11 h-11 rounded-lg bg-gray-200" />
        <div className="w-11 h-11 rounded-lg bg-gray-200" />
      </div>

      {/* Priority Indicator Skeleton */}
      <div className="absolute top-2 right-2 w-8 h-8 rounded-full bg-gray-200" />
    </div>
  );
}

/**
 * Skeleton Task List Component
 *
 * Shows multiple skeleton task cards during initial load.
 *
 * @param count - Number of skeleton cards to show
 */
export function SkeletonTaskList({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-4 animate-fade-in">
      {Array.from({ length: count }).map((_, index) => (
        <div
          key={index}
          className="animate-slide-in-up"
          style={{
            animationDelay: `${index * 100}ms`,
            animationFillMode: "both"
          }}
        >
          <SkeletonTaskCard />
        </div>
      ))}
    </div>
  );
}

/**
 * Delete task confirmation modal client component.
 *
 * Displays an AlertDialog for delete confirmation to prevent accidental deletions.
 * Implements keyboard navigation:
 * - Escape key closes modal
 * - Enter key confirms delete
 * - Tab cycles between Cancel and Delete buttons
 */
"use client";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface DeleteTaskModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  taskTitle: string;
  onConfirmDelete: () => void;
}

export function DeleteTaskModal({
  open,
  onOpenChange,
  taskTitle,
  onConfirmDelete,
}: DeleteTaskModalProps) {
  // Handle keyboard events
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      onConfirmDelete();
    } else if (e.key === "Escape") {
      e.preventDefault();
      onOpenChange(false);
    }
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent onKeyDown={handleKeyDown}>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Task?</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete &quot;{taskTitle}&quot;? This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel className="min-h-[44px] min-w-[44px]">
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirmDelete}
            className="bg-red-600 hover:bg-red-700 min-h-[44px] min-w-[44px]"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

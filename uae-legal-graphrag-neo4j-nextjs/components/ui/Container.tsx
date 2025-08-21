import * as React from "react";

export function Container({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`mx-auto w-full px-[var(--page-pad)] max-w-[min(var(--max-page),100vw)] ${className}`}
      {...props}
    />
  );
}

export default Container;

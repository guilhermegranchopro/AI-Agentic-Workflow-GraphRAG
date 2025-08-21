import * as React from "react";

export function Container({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`mx-auto w-full max-w-6xl px-3 sm:px-4 lg:px-6 ${className}`}
      {...props}
    />
  );
}

export default Container;

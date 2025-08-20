import * as React from "react";

export function Container({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`mx-auto w-full max-w-screen-2xl px-4 sm:px-6 lg:px-8 ${className}`}
      {...props}
    />
  );
}

export default Container;

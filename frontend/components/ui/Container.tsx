import * as React from "react";

export function Container({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`prof-container ${className}`}
      {...props}
    />
  );
}

export default Container;

import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html 
      className="h-full" 
      style={{ 
        background: "var(--app-bg, #0b0b0b)", 
        overscrollBehavior: "none" 
      }}
    >
      <Head />
      <body className="h-full overflow-hidden">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

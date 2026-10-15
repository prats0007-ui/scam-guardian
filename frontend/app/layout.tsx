import type { Metadata } from "next";
import { Atkinson_Hyperlegible } from "next/font/google";
import "./globals.css";

// Atkinson Hyperlegible was designed by the Braille Institute for low-vision
// readers, so letters like I, l and 1 are easy to tell apart.
const atkinson = Atkinson_Hyperlegible({ subsets: ["latin"], weight: ["400", "700"] });

export const metadata: Metadata = {
  title: "Scam Guardian",
  description: "Check a suspicious message before you click.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={atkinson.className}>{children}</body>
    </html>
  );
}

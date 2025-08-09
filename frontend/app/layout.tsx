import React from 'react'
import './globals.css'

export const metadata = {
  title: 'AI Code Review Bot',
  description: 'Automatic pull-request reviews powered by GPT-4o',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-neutral-950 text-neutral-100">{children}</body>
    </html>
  )
}

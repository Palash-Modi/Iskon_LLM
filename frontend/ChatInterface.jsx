"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Sun, Moon } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { motion } from "framer-motion";
import "tailwindcss/tailwind.css";

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => setDarkMode(!darkMode);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();

      const assistantMessage = {
        type: "assistant",
        text: data.answer,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = {
        type: "assistant",
        text: "⚠️ Sorry, something went wrong!",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div className={`${darkMode ? "dark" : ""} min-h-screen bg-gray-100 dark:bg-zinc-900 text-zinc-900 dark:text-white transition`}>
      <div className="max-w-2xl mx-auto py-6 px-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">📖 Vedabase Chat</h1>
          <Button onClick={toggleTheme} variant="ghost" size="icon">
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </Button>
        </div>

        {/* Chat Box */}
        <Card className="h-[70vh] overflow-hidden">
          <CardContent className="p-4 h-full">
            <ScrollArea className="h-full pr-4 space-y-4">
              {messages.map((msg, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div
                    className={`rounded-xl p-3 whitespace-pre-line ${
                      msg.type === "user"
                        ? "bg-blue-100 dark:bg-blue-900"
                        : "bg-zinc-200 dark:bg-zinc-800"
                    }`}
                  >
                    <p dangerouslySetInnerHTML={{ __html: msg.text }}></p>
                  </div>
                </motion.div>
              ))}
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Input Box */}
        <div className="mt-4 flex gap-2">
          <Input
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />
          <Button onClick={handleSubmit}>Send</Button>
        </div>
      </div>
    </div>
  );
}

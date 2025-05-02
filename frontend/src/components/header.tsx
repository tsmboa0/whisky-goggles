import React from "react";
import { Link } from "wouter";
import { useTheme } from "next-themes";
import { Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Header() {
  const { theme, setTheme } = useTheme();

  return (
    <header className="text-center py-8 md:py-12 relative">
      {/* Theme Toggle Button */}
      <div className="absolute right-4 top-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="rounded-full w-10 h-10 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="h-5 w-5 text-yellow-500" />
          ) : (
            <Moon className="h-5 w-5 text-gray-700" />
          )}
        </Button>
      </div>
      
      <div className="flex flex-col items-center">
        <Link href="/">
          <div className="flex flex-col items-center">
            <img 
              src="https://res.cloudinary.com/dgvnuwspr/image/upload/v1740441389/wdqjosbtpgjiyi1ovups.png"
              alt="BAXUS Logo" 
              className="w-28 h-28 mb-4 logo-animation"
            />
            <h1 className="text-4xl md:text-5xl font-bold gradient-text mb-3">
              Whisky Bottle Scanner
            </h1>
          </div>
        </Link>
      </div>
      <div className="w-32 h-1 mx-auto my-4 bg-primary/30 rounded"></div>
      <p className="text-gray-600 dark:text-gray-300 mt-2 text-lg max-w-2xl mx-auto">
        Discover detailed information about any whisky bottle by simply uploading a photo
      </p>
    </header>
  );
}

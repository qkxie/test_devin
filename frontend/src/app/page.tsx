"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
  };

  const handleAnalyze = () => {
    if (selectedFile) {
      console.log("开始分析文件:", selectedFile.name);
    } else {
      alert("请先选择一个文件");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <Card className="w-full max-w-md mx-auto shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-200">
            数据分析平台
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="file-upload" className="text-sm font-medium text-slate-700 dark:text-slate-300">
              选择文件
            </label>
            <Input
              id="file-upload"
              type="file"
              onChange={handleFileChange}
              className="cursor-pointer"
              accept=".csv,.xlsx,.json,.txt"
            />
            {selectedFile && (
              <p className="text-sm text-slate-600 dark:text-slate-400">
                已选择: {selectedFile.name}
              </p>
            )}
          </div>
          <Button 
            onClick={handleAnalyze}
            className="w-full"
            size="lg"
          >
            开始分析
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

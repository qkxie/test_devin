"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Copy } from "lucide-react";
import { toast } from "sonner";

interface AnalysisResult {
  filename: string;
  status: string;
  summary: {
    total_users: number;
    eligible_users: number;
    eligibility_rate: number;
    overall_avg_score: number;
  };
  location_stats: {
    [key: string]: {
      count: number;
      avg_score: number;
      eligible: number;
    };
  };
  detailed_results: Array<{
    Name: string;
    Location: string;
    avg_score: number;
    EligibleStatus: string;
  }>;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setAnalysisResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("请先选择一个文件");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('https://data-analysis-api-askupnki.fly.dev/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '分析失败');
      }

      const result: AnalysisResult = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '分析过程中发生错误');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyResults = async () => {
    if (!analysisResult) return;
    
    try {
      await navigator.clipboard.writeText(JSON.stringify(analysisResult, null, 2));
      toast("已复制到剪贴板");
    } catch (err) {
      toast("复制失败，请重试");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl mx-auto space-y-6">
        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-200">
              数据分析平台
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file-upload" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                选择CSV文件
              </label>
              <Input
                id="file-upload"
                type="file"
                onChange={handleFileChange}
                className="cursor-pointer"
                accept=".csv"
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
              disabled={isLoading || !selectedFile}
            >
              {isLoading ? "分析中..." : "开始分析"}
            </Button>
            
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}
          </CardContent>
        </Card>

        {analysisResult && (
          <Card className="shadow-lg">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="text-xl font-bold text-slate-800 dark:text-slate-200">
                分析结果
              </CardTitle>
              <Button
                onClick={handleCopyResults}
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                <Copy className="h-4 w-4" />
                复制结果
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-600 font-medium">总用户数</p>
                  <p className="text-2xl font-bold text-blue-800">{analysisResult.summary.total_users}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-green-600 font-medium">符合条件</p>
                  <p className="text-2xl font-bold text-green-800">{analysisResult.summary.eligible_users}</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="text-sm text-purple-600 font-medium">合格率</p>
                  <p className="text-2xl font-bold text-purple-800">{analysisResult.summary.eligibility_rate}%</p>
                </div>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <p className="text-sm text-orange-600 font-medium">平均分</p>
                  <p className="text-2xl font-bold text-orange-800">{analysisResult.summary.overall_avg_score}</p>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">城市统计</h3>
                <div className="space-y-4">
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={Object.entries(analysisResult.location_stats).map(([location, stats]) => ({
                          location,
                          count: stats.count,
                          avg_score: stats.avg_score,
                          eligible: stats.eligible
                        }))}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                        <XAxis 
                          dataKey="location" 
                          className="text-sm"
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis 
                          className="text-sm"
                          tick={{ fontSize: 12 }}
                        />
                        <Tooltip 
                          contentStyle={{
                            backgroundColor: 'white',
                            border: '1px solid #e2e8f0',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                          }}
                          formatter={(value, name) => {
                            const labels = {
                              count: '用户数',
                              avg_score: '平均分',
                              eligible: '合格人数'
                            };
                            return [value, labels[name as keyof typeof labels] || name];
                          }}
                        />
                        <Bar dataKey="count" fill="#3b82f6" name="count" />
                        <Bar dataKey="avg_score" fill="#10b981" name="avg_score" />
                        <Bar dataKey="eligible" fill="#8b5cf6" name="eligible" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="space-y-2">
                    {Object.entries(analysisResult.location_stats).map(([location, stats]) => (
                      <div key={location} className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                        <span className="font-medium">{location}</span>
                        <div className="text-sm text-slate-600">
                          {stats.count}人 | 平均分: {stats.avg_score} | 合格: {stats.eligible}人
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">详细结果</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left p-2">姓名</th>
                        <th className="text-left p-2">城市</th>
                        <th className="text-left p-2">平均分</th>
                        <th className="text-left p-2">是否合格</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysisResult.detailed_results.map((user, index) => (
                        <tr key={index} className="border-b">
                          <td className="p-2">{user.Name}</td>
                          <td className="p-2">{user.Location}</td>
                          <td className="p-2">{user.avg_score.toFixed(1)}</td>
                          <td className="p-2">
                            <span className={`px-2 py-1 rounded text-xs ${
                              user.EligibleStatus === 'YES' 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {user.EligibleStatus === 'YES' ? '合格' : '不合格'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

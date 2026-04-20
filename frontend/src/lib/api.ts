import type { FileItem, AlertItem } from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function fetchFiles(): Promise<FileItem[]> {
  const res = await fetch(`${BASE_URL}/files`, { cache: "no-store" });
  if (!res.ok) throw new Error("Не удалось загрузить файлы");
  return res.json() as Promise<FileItem[]>;
}

export async function fetchAlerts(): Promise<AlertItem[]> {
  const res = await fetch(`${BASE_URL}/alerts`, { cache: "no-store" });
  if (!res.ok) throw new Error("Не удалось загрузить алерты");
  return res.json() as Promise<AlertItem[]>;
}

export async function uploadFile(title: string, file: File): Promise<FileItem> {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/files`, { method: "POST", body: formData });
  if (!res.ok) throw new Error("Не удалось загрузить файл");
  return res.json() as Promise<FileItem>;
}

export function getDownloadUrl(fileId: string): string {
  return `${BASE_URL}/files/${fileId}/download`;
}

import type { NextApiRequest, NextApiResponse } from "next";
import { getConfig, getConfigKeys } from "../../../lib/config";

interface DiagnosticsResponse {
  ok: boolean;
  message?: string;
  present: Record<string, boolean>;
}

export default function handler(req: NextApiRequest, res: NextApiResponse<DiagnosticsResponse>) {
  if (req.method !== 'GET') {
    return res.status(405).json({
      ok: false,
      message: 'Method not allowed',
      present: {}
    });
  }

  try {
    const cfg = getConfig();
    const mask = Object.fromEntries(getConfigKeys().map(k => [k, true]));
    res.status(200).json({ ok: true, present: mask });
  } catch (e: any) {
    res.status(200).json({ 
      ok: false, 
      message: e.message, 
      present: e.present ?? {} 
    });
  }
}

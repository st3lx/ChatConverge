
---

## 2) `shared/ipc-types.ts`
```ts
// shared/ipc-types.ts
export type ImportResult =
  | { error: string }
  | { platform?: string; messages?: Array<NormalizedMessage> };

export type NormalizedMessage = {
  timestamp: string;
  sender: string;
  text: string;
  attachments?: string[];
};

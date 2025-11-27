// small helper for calling backend directly (not used by importDialog)
import axios from "axios";

export async function importChatPath(path: string) {
  const resp = await axios.post("http://127.0.0.1:8000/import", { path });
  return resp.data;
}

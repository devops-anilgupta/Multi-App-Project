let config = null;

export async function loadConfig() {
  let url;
  if (process.env.NODE_ENV === "development") {
    url = "http://localhost:5000/config"; // Dev: point to backend directly
  } else {
    url = "/config"; // Prod: served by same domain
  }

  const res = await fetch(url);
  config = await res.json();
  console.log("Loaded config:", config); // Shows in browser console
}

export function getApiUrl() {
  return config?.API_URL;
}

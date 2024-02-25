
async function makeLocalFetch(url, data, headers = {}, method = "POST") {

    const headers = new Headers(headers);
    headers.append("Content-Type", "application/json");

    const response = await fetch(url, {
        method: method,
        mode: "cors",
        credentials: "same-origin",
        headers: headers,
        body: data
    });

    return response;
}

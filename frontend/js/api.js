const API = (() => {
  async function request(path, options={}) {
    const token = localStorage.getItem('campusspace_token');
    const headers = {Accept:'application/json', ...(options.headers||{})};
    if (token) headers.Authorization = `Bearer ${token}`;
    if (options.body && !(options.body instanceof FormData) && typeof options.body !== 'string') {headers['Content-Type']='application/json';options={...options,body:JSON.stringify(options.body)};}
    const response = await fetch(`${API_CONFIG.BASE_URL}${path}`, {...options,headers});
    const ct = response.headers.get('content-type')||'';
    const body = response.status===204 ? null : (ct.includes('application/json') ? await response.json() : await response.text());
    if(!response.ok) throw new Error((body && (body.detail||body.message)) || `Request failed (${response.status})`);
    return body;
  }
  return {request};
})();

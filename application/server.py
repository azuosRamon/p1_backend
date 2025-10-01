from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, re, os
from domain.category import Category
from domain.movie import Movie
from infra.json_repo import JsonRepo

# ---- Repositórios com persistência em ./data/*.json ----
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CAT_PATH = os.path.join(DATA_DIR, 'categories.json')
MOV_PATH = os.path.join(DATA_DIR, 'movies.json')
cat_repo = JsonRepo(
    path=CAT_PATH,
    to_dict=lambda c: c.__dict__,
    from_dict=lambda d: Category(**d),
)

mov_repo = JsonRepo(
    path=MOV_PATH,
    to_dict=lambda m: m.__dict__,
    from_dict=lambda d: Movie(**d),
)

class JsonHandler(BaseHTTPRequestHandler):
    # ---------- utilitários ----------
    def _json(self, status: int, payload: dict | list):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _parse_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except json.JSONDecodeError:
            return {}
    # ---------- GET ----------
    def do_GET(self):
        path = self.path
        # /categories e /categories/{id}
        if path == '/categories':
            return self._json(200, [c.__dict__ for c in cat_repo.list()])
        m = re.match(r'^/categories/([\w-]+)$', path)
        if m:
            cid = m.group(1)
            c = cat_repo.get(cid)
            return self._json(200, c.__dict__) if c else self._json(404,{"error": "category not found"})
        # /movies e /movies/{id}
        if path == '/movies':
            return self._json(200, [m.__dict__ for m in mov_repo.list()])
        m = re.match(r'^/movies/([\w-]+)$', path)
        if m:
            mid = m.group(1)
            mv = mov_repo.get(mid)
            return self._json(200, mv.__dict__) if mv else self._json(404,{"error": "movie not found"})
        return self._json(404, {"error": "not found"})
    
    # ---------- POST ----------
    def do_POST(self):
        path = self.path
        data = self._parse_body()
        # Criar Category
        if path == '/categories':
            try:
                # NÃO passamos id quando não vier -> Category gera sozinho
                kwargs = {
                    "name": data.get("name", ""),
                    "description": data.get("description", ""),
                    "is_active": data.get("is_active", True),
                }
                if data.get("id"): # se quiser criar com id fixo em testes
                    kwargs["id"] = data["id"]
                c = Category(**kwargs)
                cat_repo.add(c)
                return self._json(201, c.__dict__)
            
            except Exception as e:
                return self._json(400, {"error": str(e)})
        
        # Ativar/Desativar Category
        m = re.match(r'^/categories/([\w-]+)/(activate|deactivate)$', path)
        if m:
            cid, action = m.group(1), m.group(2)
            c = cat_repo.get(cid)
            if not c:
                return self._json(404, {"error": "category not found"})
            c.activate() if action == 'activate' else c.deactivate()
            cat_repo.update(c)
            return self._json(200, c.__dict__)
        
        # Criar Movie
        if path == '/movies':
            try:
                cat_id = data.get('category_id')
                if not cat_id or not cat_repo.get(cat_id):
                    return self._json(400, {"error": "category_id inválido/inexistente"})
                kwargs = {
                    "title": data.get("title", ""),
                    "year": int(data.get("year", 0)),
                    "category_id": cat_id,
                    "description": data.get("description", ""),
                    "is_active": data.get("is_active", True),
                }
                if data.get("id"):
                    kwargs["id"] = data["id"]
                mobj = Movie(**kwargs)
                mov_repo.add(mobj)
                return self._json(201, mobj.__dict__)
            except Exception as e:
                return self._json(400, {"error": str(e)})
            
        return self._json(404, {"error": "not found"})
    
    # ---------- PUT ----------
    def do_PUT(self):
        # Atualizar Category (name/description)
        m = re.match(r'^/categories/([\w-]+)$', self.path)
        if m:
            cid = m.group(1)
            c = cat_repo.get(cid)
            if not c:
                return self._json(404, {"error": "category not found"})
            data = self._parse_body()
            try:
                c.update(name=data.get('name'),description=data.get('description'))
                cat_repo.update(c)
                return self._json(200, c.__dict__)
            except Exception as e:
                return self._json(400, {"error": str(e)})
        
        # Atualizar Movie
        m = re.match(r'^/movies/([\w-]+)$', self.path)
        if m:
            mid = m.group(1)
            mv = mov_repo.get(mid)
            if not mv:
                return self._json(404, {"error": "movie not found"})
            data = self._parse_body()
            try:
                cat_id = data.get('category_id')
                if cat_id and not cat_repo.get(cat_id):
                    return self._json(400, {"error": "category_id inválido/inexistente"})
                mv.update(
                    title=data.get('title'),
                    description=data.get('description'),
                    year=data.get('year'),
                    category_id=cat_id
                )
                mov_repo.update(mv)
                return self._json(200, mv.__dict__)
            except Exception as e:
                return self._json(400, {"error": str(e)})
        return self._json(404, {"error": "not found"})
        
    # ---------- DELETE ----------
    def do_DELETE(self):
        
        # Deletar Category
        m = re.match(r'^/categories/([\w-]+)$', self.path)
        if m:
            cid = m.group(1)
            # Regra de negócio: não pode deletar categoria com filmes associados
            if any(m.category_id == cid for m in mov_repo.list()):
                return self._json(400, {"error": "não pode deletar categoria com filmes associados"})
            cat_repo.delete(cid)
            return self._json(204, {})
        
        # Deletar Movie
        m = re.match(r'^/movies/([\w-]+)$', self.path)
        if m:
            mid = m.group(1)
            mov_repo.delete(mid)
            return self._json(204, {})
        return self._json(404, {"error": "not found"})
        
    def run(server_class=HTTPServer, handler_class=JsonHandler, port=8000):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f'Servidor HTTP rodando em http://localhost:{port}')
        httpd.serve_forever()
    
    if __name__ == '__main__':
        run()
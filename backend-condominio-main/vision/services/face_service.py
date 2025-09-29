""" import numpy as np
from django.conf import settings
from django.db.models import Q
from insightface.app import FaceAnalysis
from vision.utils.images import decode_data_url, save_pil_image
from ..models import FaceProfile, FaceEvent

# Carga única del modelo (en el primer uso del worker/proceso)
_app = None

def _get_app():
    global _app
    if _app is None:
        _app = FaceAnalysis(name="buffalo_l")  # modelo ArcFace
        # ctx_id = 0 usa GPU si existe; -1 = CPU. onnxruntime usa CPU por defecto.
        _app.prepare(ctx_id=0, det_size=(640, 640))
    return _app

def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))

def _embedding_from_pil(img_pil):
    app = _get_app()
    img = np.array(img_pil)[:, :, ::-1]  # RGB->BGR
    faces = app.get(img)
    if not faces:
        return None, 0, None
    # Tomar el rostro con mayor score
    face = max(faces, key=lambda f: float(f.det_score))
    emb = face.normed_embedding.astype(np.float32)  # (512,)
    return emb, float(face.det_score), face

def enroll_face(usuario_id: int, data_urls: list[str], label: str = "principal"):
    saved = []
    for data_url in data_urls:
        img = decode_data_url(data_url)
        emb, det_score, face = _embedding_from_pil(img)
        if emb is None:
            continue
        # Guardar recorte opcional: aquí usamos la imagen completa
        rel_path = save_pil_image(img, subdir="faces/enroll", prefix=f"user{usuario_id}")
        FaceProfile.objects.create(
            usuario_id=usuario_id,
            label=label,
            embedding=emb.tobytes(),
            vector_dim=len(emb),
        )
        saved.append({"foto_path": rel_path, "det_score": det_score})
    return {"total": len(data_urls), "guardadas": len(saved), "items": saved}

def recognize_face(data_url: str, umbral: float | None = None):
    umbral = float(umbral) if umbral is not None else float(getattr(settings, "FACE_THRESHOLD", 0.5))
    img = decode_data_url(data_url)
    emb, det_score, _ = _embedding_from_pil(img)
    rel_path = save_pil_image(img, subdir="faces/recognize", prefix="probe")
    if emb is None:
        FaceEvent.objects.create(usuario=None, confianza=0.0, foto_path=rel_path, aceptado=False, motivo="SIN_ROSTRO")
        return {"match": False, "confianza": 0.0, "usuario_id": None, "foto_path": rel_path, "motivo": "SIN_ROSTRO"}

    # Comparar contra todos los embeddings
    best_uid, best_sim = None, -1.0
    for fp in FaceProfile.objects.all().only("id", "usuario_id", "embedding", "vector_dim"):
        ref = np.frombuffer(fp.embedding, dtype=np.float32)
        if ref.shape[0] != emb.shape[0]:  # por si cambiaste de modelo
            continue
        sim = _cosine_sim(emb, ref)
        if sim > best_sim:
            best_sim, best_uid = sim, fp.usuario_id

    match = best_sim >= umbral
    ev = FaceEvent.objects.create(
        usuario_id=best_uid if match else None,
        confianza=best_sim if best_sim > 0 else 0.0,
        foto_path=rel_path,
        aceptado=match,
        motivo="MATCH_OK" if match else "SIN_MATCH",
    )
    return {
        "match": match,
        "usuario_id": best_uid if match else None,
        "confianza": round(best_sim, 4),
        "evento_id": ev.id,
        "foto_path": rel_path,
        "umbral": umbral,
    }
 """
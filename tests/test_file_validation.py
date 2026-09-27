from app.services.file import _signature_matches


def test_supported_signatures():
    assert _signature_matches(".pdf", b"%PDF-1.7")
    assert _signature_matches(".png", b"\x89PNG\r\n\x1a\nrest")
    assert _signature_matches(".jpg", b"\xff\xd8\xffrest")
    assert _signature_matches(".webp", b"RIFFxxxxWEBPrest")
    assert _signature_matches(".doc", b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1rest")
    assert _signature_matches(".docx", b"PK\x03\x04rest")


def test_invalid_signature_rejected():
    assert not _signature_matches(".pdf", b"not a pdf")
    assert not _signature_matches(".png", b"not an image")

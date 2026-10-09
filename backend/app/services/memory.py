from backend.app.services.rag.vectordb import clear

_memory = {}


def get_history(session_id: str):
    return _memory.get(session_id, [])


def add_message(
    session_id: str,
    role: str,
    content: str,
):
    if session_id not in _memory:
        _memory[session_id] = []

    _memory[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_history(session_id: str):
    _memory.pop(session_id, None)

    clear(session_id)
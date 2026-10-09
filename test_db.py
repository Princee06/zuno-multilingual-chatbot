from backend.app.services.rag.vectordb import collection


count = collection.count()

print("Documents in DB:", count)


if count > 0:

    data = collection.get(
        limit=3
    )

    print(data)
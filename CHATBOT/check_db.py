import chromadb

print("🔍 Inspecting local ChromaDB...")

try:
    # Connect to your existing local database folder
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
   
    # Grab the collection we created in core_engine
    collection = chroma_client.get_collection(name="clinical_frameworks")
   
    # Fetch all the documents currently saved in it
    data = collection.get()
   
    print(f"\n✅ SUCCESS! Found {len(data['documents'])} frameworks saved in the database.\n")
   
    # Print them out nicely
    for i, doc in enumerate(data['documents']):
        print(f"Framework {i+1}: {doc}")

except Exception as e:
    print(f"\n❌ ERROR: Could not read database. Reason: {e}")
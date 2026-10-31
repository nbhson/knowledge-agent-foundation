// Retrieve relevant context
const relevantDocs = await vectorDB.search(query);
const context = relevantDocs.map(doc => doc.content).join('\n');

// Add to prompt
const prompt = `Context: ${context}\n\nQuestion: ${query}`;

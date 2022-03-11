word2id = model.wv.key_to_index  # (8507)
for k in word2id.keys():
    word2id[k] += len(special_tokens)
for i in range(len(special_tokens)):
    word2id[special_tokens[i]] = i

vector_size = model.wv.vector_size
vocab_size = len(word2id)
special_token_vec = np.zeros(
    (len(special_tokens), vector_size))
vectors = model.wv.vectors  # (8507, 300)
vectors = np.concatenate(
    (special_token_vec, vectors))  # (8511, 300)

# AUTOGENERATED! DO NOT EDIT! File to edit: 04_LM_with_normalized_embeddings.ipynb (unless otherwise specified).

__all__ = ['PermuteEmbeddingNorm', 'p_normAWD_LSTM']

# Cell
class PermuteEmbeddingNorm(nn.Module):
    def __init__(self, num_embeddings, embedding_dim, padding_idx):
        super().__init__()

        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.padding_idx = padding_idx

        # to conform to nn.Embedding api
        self.max_norm=None
        self.norm_type=2.0
        self.scale_grad_by_freq=False
        self.sparse = False

        self.weight = nn.Parameter( torch.Tensor(num_embeddings, embedding_dim) )
        nn.init.kaiming_uniform_(self.weight)
        self.p = nn.Parameter( torch.eye(self.num_embeddings) )
        self.p.requires_grad = False

        self.reset_parameters()

    def forward(self, words):
        return F.embedding(words, self.p @ self.normalized_weight())

    def normalized_weight(self):
        w1 = self.weight / self.weight.norm(dim=1).unsqueeze(1)
        w2 = w1 - w1.mean(0)
        w3 = w2 / w2.norm(dim=1).unsqueeze(1)
        return w3

    def reset_parameters(self): pass

# Cell
class p_normAWD_LSTM(AWD_LSTM):
    def __init__(self, vocab_sz, emb_sz, n_hid, n_layers, pad_token=1, hidden_p=0.2, input_p=0.6, embed_p=0.1,
                 weight_p=0.5, bidir=False, packed=False):
        store_attr(self, 'emb_sz,n_hid,n_layers,pad_token,packed')
        self.bs = 1
        self.n_dir = 2 if bidir else 1
        self.encoder = PermuteEmbeddingNorm(vocab_sz, emb_sz, padding_idx=pad_token)
        self.encoder_dp = self.encoder
        self.rnns = nn.ModuleList([self._one_rnn(emb_sz if l == 0 else n_hid, (n_hid if l != n_layers - 1 else emb_sz)//self.n_dir,
                                                 bidir, weight_p, l) for l in range(n_layers)])
        self.encoder.weight.data.uniform_(-self.initrange, self.initrange)
        self.input_dp = RNNDropout(input_p)
        self.hidden_dps = nn.ModuleList([RNNDropout(hidden_p) for l in range(n_layers)])
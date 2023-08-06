## Linear Attention

<img src="./linear-attention.png"/>

[![PyPI version](https://badge.fury.io/py/linear-attention.svg)](https://badge.fury.io/py/linear-attention-transformer)

A repository that hosts a collection of tools for a variant of attention that is linear with respect to the sequence length.

I haven't found it to be good enough to serve as a language model, but it still performs decently enough that it could complement / augment regular attention in identifying global patterns, or as a last resort under resource-limited settings.

## Install

```bash
$ pip install linear-attention
```

## Usage

For regular sequences in the form of `(batch, seqlen, dim)`

```python
import torch
import torch.nn.functional as F
from linear_attention.linear_attention import LinearSelfAttention

attn = LinearSelfAttention(
    dim = 512,
    heads = 8,
    causal = True,
    one_kv_head = True,           # share a single key/value head for all query heads, to save on memory
    psi_fn = lambda x: F.relu(x)  # customize the psi function from the 'Transformer is RNN' paper
)

x = torch.randn(1, 1024, 512)
attn(x) # (1, 1024, 512)
```

For images

```python
import torch
import torch.nn.functional as F
from linear_attention.linear_attention import LinearImageAttention

attn = LinearImageAttention(
    chan = 32,
    heads = 8,
    key_dim = 64     # dimension keys, can be downgraded to 32 to save even more memory
)

img = torch.randn(1, 32, 512, 512)
attn(img) # (1, 32, 512, 512)
```

## Citations

```bibtex
@inproceedings{katharopoulos-et-al-2020,
  author    = {Katharopoulos, A. and Vyas, A. and Pappas, N. and Fleuret, F.},
  title     = {Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention},
  booktitle = {Proceedings of the International Conference on Machine Learning (ICML)},
  year      = {2020},
  note      = {(to appear)}
}
```

```bibtex
@article{shen2019efficient,
  author    = {Zhuoran Shen and
               Mingyuan Zhang and
               Haiyu Zhao and
               Shuai Yi and
               Hongsheng Li},
  title     = {Efficient Attention: Attention with Linear Complexities},
  journal   = {CoRR},
  volume    = {abs/1812.01243},
  year      = {2018},
  url       = {http://arxiv.org/abs/1812.01243}
}
```

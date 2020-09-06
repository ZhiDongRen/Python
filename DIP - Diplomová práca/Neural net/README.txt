Reconstruction of damaged fingerprint using autoeconder neural net
Author: xhalin01

Requirements: python 3.6.8, CUDA 10.0 and other described in requirements.txt 

Training of autoencoder:

- images must have 400x256px as shown examples in pure/damaged - created by anguli, and with inserted wart from SyFDaS
  https://www.fit.vut.cz/research/product/600/.cs,
- for better quality of output fingerprint images, 3 iterations of learning and reconstructing are recommended
